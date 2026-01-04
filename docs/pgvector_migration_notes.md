# pgvector Migration Notes

## 1. Current DB Initialization

- **Engine**: `src.database.engine`. Created via `sqlalchemy.create_engine`.
- **Session lifecycle**: `src.database.SessionLocal` is `sessionmaker(autocommit=False, autoflush=False)`. Dependency `get_db` yields session and closes it in finally block.
- **Database URL source**: `settings.DATABASE_URL` (from `src.config.settings`). Defaults to `sqlite:///./victus.db`.
- **SQLite file path assumptions**: Relative path `./victus.db` in existing configuration. Also `alembic.ini` hardcodes `sqlite:///./chat_history.db` but `env.py` overrides it with `settings.DATABASE_URL`.

## 2. Alembic Configuration

- **alembic.ini summary**: Standard config. `script_location = alembic`. `sqlalchemy.url` is present but overridden by `env.py`.
- **env.py target_metadata**: `src.database.Base.metadata`.
- **How DB URL is loaded**: `settings.DATABASE_URL` is imported from `src.config` and passed to `config.set_main_option("sqlalchemy.url", ...)`.
- **Migration files list**:
  - `993afe580406_refactor_models_to_package_with_new_.py`
  - `ec4f65823ae4_add_oauth_accounts.py`
  - `6dd9452c10a1_add_safety_tables.py`
  - `4f95b897a5b8_add_password_reset_tokens.py`

## 3. Existing Schema Summary

- **Tables**:
  - `users`: Core user table.
  - `conversations`: Chat sessions.
  - `messages`: Chat history (standard rows).
  - `conversation_memories`: Stores summarization state (text summary, last summarized message ID).
  - `user_facts`: Simple Key-Value store (user_id, key, value) for long-term memory.
  - `documents`: Metadata for uploaded files (path, filename).
  - `traces`, `trace_steps`: Observability/Evaluation tables.
  - `pending_actions`: Human-in-the-loop approvals.
  - `oauth_accounts`, `passkeys`, `password_reset_tokens`: Auth tables.
- **Notable constraints**:
  - `conversations.user_id` -> `users.id` (CASCADE).
  - `messages.conversation_id` -> `conversations.id` (CASCADE).
  - `conversation_memories.conversation_id` -> `conversations.id` (Unique, CASCADE).
- **Notes on model vs migration mismatches**: None observed. Models in `src/models/*.py` seem to match the migrations.

## 4. Current Memory Implementation

- **Memory entry points**:
  - `src.tools.memory_tools.remember_fact`: Stores key-value fact in SQL (`user_facts`).
  - `src.tools.memory_tools.recall_fact`: Retrieves key-value fact from SQL.
  - `src.tools.rag_tools.query_uploaded_documents`: Retrieval from FAISS index.
  - `src.tools.rag_tools.update_vector_store`: Ingestion into FAISS index.
  - `src.agent.memory.ConversationContextManager`: Handles summarization (LLM-based, not vector) and fetches raw messages/summary from SQL.
- **Where memory is stored (DB/files)**:
  - Conversation History & Summaries: SQL (`conversations`, `messages`, `conversation_memories`).
  - Facts: SQL (`user_facts`).
  - Uploaded Documents: FAISS index file (`faiss_index/`).
- **FAISS index type + metric**:
  - Managed by `langchain_community.vectorstores.FAISS`.
  - Type: Default `IndexFlatL2` (implied by `FAISS.from_documents` default behavior).
  - Metric: L2 (Euclidean distance). Since OpenAI embeddings are unit-normalized, this is equivalent to Cosine similarity ranking (though scores differ).
- **Index persistence paths**: Directory `faiss_index/` (relative to backend root). Code checks `os.listdir(FAISS_INDEX_PATH)`.
- **Metadata persistence**: Stored inside the FAISS index (LangChain serialization includes `docstore` and `index_to_docstore_id`).
- **Retrieval logic**:
  - Top-k: `k=3` (hardcoded in `_query_uploaded_documents`).
  - Scoring: "similarity" (L2 distance acting as similarity search).
  - Filters: None currently used in retrieval.
- **User scoping**:
  - Facts: Scoped by `user_id`.
  - Documents (RAG): **SINGLE TENANT / UNSCOPED**. `query_uploaded_documents` queries the _entire_ `faiss_index` without filtering by `user_id`, even though `Document` table has `user_id`. This is a risk.

## 5. Embedding Provider

- **Provider + model**: `langchain_openai.OpenAIEmbeddings` using model `text-embedding-3-small`.
- **Dimension**: 1536 (Standard for this model).
- **Normalization**: OpenAI embeddings are unit-normalized by the API.
- **Where embedding is called from**: `src.tools.rag_tools` (for both `update_vector_store` and `query_uploaded_documents`).

## 6. Tests and Behavioral Contracts

- **Relevant test files**:
  - `backend/tests/test_memory_tools.py`: Tests `remember_fact` (SQL) logic. Mocks DB session.
  - `backend/tests/test_agent.py`: Tests agent creation, mocks tools.
- **What each test asserts**:
  - `test_memory_tools.py`: Asserts that `remember_fact` updates or adds a record in DB and returns correct string message.
- **Fixtures and setup assumptions**:
  - `test_memory_tools.py` uses `patch('src.tools.memory_tools.SessionLocal')`. This mock must be updated or replaced if `SessionLocal` changes or if we move to `pgvector` for facts (though facts seem to stay SQL).
  - No existing tests specifically for FAISS behavior or `rag_tools` were found in `backend/tests/`.

## 7. Migration Implications for pgvector

- **Items we must preserve**:
  - `remember_fact` and `recall_fact` return strings (agent relies on this textual feedback).
  - `query_uploaded_documents` returns string summary of documents.
  - `ConversationContextManager`'s summarization Logic (SQL-based) can remain as is, or be augmented with vector search later.
- **Items we can change safely later**:
  - Move `user_facts` to vector store semantic search instead of exact key match (future).
  - **CRITICAL**: The current `rag_tools` implementation is not user-scoped. Migration to pgvector MUST introduce `user_id` filtering to fix the data leak risk.

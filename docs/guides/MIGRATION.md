# Migration Guide: v1.0 to v2.0

This guide helps you migrate from Project VICTUS v1.0 to v2.0.

## Major Changes

### 1. Package Structure
- **Old**: Flat file structure with relative imports
- **New**: Proper package structure under `src/` directory
- **Action**: Update all imports to use `src.` prefix

### 2. AI Model
- **Old**: Google Gemini (`langchain-google-genai`)
- **New**: OpenAI GPT-4o (`langchain-openai`)
- **Action**: 
  - Update `.env` file: Change `GOOGLE_API_KEY` to `OPENAI_API_KEY`
  - Get your OpenAI API key from https://platform.openai.com

### 3. Tools Structure
- **Old**: Single `tools.py` file
- **New**: Modular `src/tools/` directory with separate files
- **Action**: No code changes needed, but be aware of new structure

### 4. Configuration
- **Old**: Direct environment variable access
- **New**: Centralized `Settings` class in `src/config.py`
- **Action**: Update `.env` file format (see `.env.example`)

### 5. Logging
- **Old**: `print()` statements
- **New**: Structured logging with `src/utils/logging.py`
- **Action**: No changes needed, but logs are now more informative

### 6. Security
- **New**: Rate limiting, CORS, input validation
- **Action**: Configure in `.env` if needed

## Migration Steps

1. **Backup your data**:
   ```bash
   cp chat_history.db chat_history.db.backup
   cp -r faiss_index faiss_index.backup
   ```

2. **Update dependencies**:
   ```bash
   poetry update
   ```

3. **Update environment variables**:
   - Copy `.env.example` to `.env`
   - Replace `GOOGLE_API_KEY` with `OPENAI_API_KEY`
   - Add any new optional keys

4. **Test the application**:
   ```bash
   poetry run uvicorn src.main:app --reload
   ```

5. **Run tests**:
   ```bash
   poetry run pytest
   ```

## Breaking Changes

- Import paths have changed (use `src.` prefix)
- `GOOGLE_API_KEY` renamed to `OPENAI_API_KEY`
- Some tool function signatures may have changed
- Database schema is compatible (no migration needed)

## Rollback

If you need to rollback:
1. Restore from backup
2. Use the old `tools.py` structure
3. Revert to Gemini in `agent.py`


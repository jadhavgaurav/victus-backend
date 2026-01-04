# Backend Readiness Analysis for UI Features

## ✅ What's Already Available

### Core Chat & Auth
- ✅ `POST /api/chat` - SSE streaming chat endpoint
- ✅ `POST /api/history` - Get chat history for a session
- ✅ `POST /api/auth/signup` - User registration
- ✅ `POST /api/auth/login` - User authentication
- ✅ `GET /api/auth/me` - Get current user profile
- ✅ `POST /api/auth/logout` - User logout
- ✅ OAuth (Google, Microsoft) - Login endpoints

### Voice Features
- ✅ `POST /api/transcribe` - Voice transcription
- ✅ `POST /api/synthesize` - Text-to-speech synthesis

### Documents
- ✅ `POST /api/upload` - Document upload for RAG

### Health & Metrics
- ✅ `GET /healthz` - Health check
- ✅ `GET /metrics` - Prometheus metrics

### Backend Tools (Available via Agent)
- ✅ Email tools (read_emails, send_email) - via M365
- ✅ Calendar tools (get_calendar_events, create_calendar_event) - via M365
- ✅ Memory tools (remember_fact, recall_fact)
- ✅ Document query (query_uploaded_documents)
- ✅ Weather tool
- ✅ Web search tool
- ✅ System tools

---

## ❌ Missing API Endpoints for UI

### 1. Conversations Management
**Required for:**
- Chat history sidebar
- Conversation list
- Delete conversations
- Export conversations

**Missing Endpoints:**
```python
GET /api/conversations
  - List all conversations/sessions for a user
  - Return: [{session_id, title, last_message, timestamp, message_count}]
  - Filter by user_id (authenticated) or session_id (unauthenticated)

DELETE /api/conversations/{session_id}
  - Delete a conversation and all its messages
  - Return: {status: "success"}

GET /api/conversations/{session_id}/export
  - Export conversation as JSON/PDF/Markdown
  - Query param: format=json|pdf|markdown
```

### 2. Documents Management
**Required for:**
- Documents manager panel
- List uploaded documents
- Delete documents
- Document status

**Missing Endpoints:**
```python
GET /api/documents
  - List all uploaded documents
  - Return: [{id, filename, size, upload_date, status, indexed}]
  - Filter by user_id if authenticated

DELETE /api/documents/{filename}
  - Delete a document
  - Remove from vector store
  - Return: {status: "success"}

GET /api/documents/status
  - Get document processing status
  - Return: {total, indexed, processing, failed}
```

### 3. Memory/Facts Management
**Required for:**
- Memory panel
- View all facts
- CRUD operations for facts

**Missing Endpoints:**
```python
GET /api/facts
  - List all user facts
  - Return: [{id, key, value, last_updated}]
  - Filter by user_id

POST /api/facts
  - Create a new fact
  - Body: {key: str, value: str}
  - Return: {id, key, value}

PUT /api/facts/{id}
  - Update an existing fact
  - Body: {key?: str, value?: str}
  - Return: {id, key, value}

DELETE /api/facts/{id}
  - Delete a fact
  - Return: {status: "success"}

GET /api/facts/export
  - Export all facts as JSON
  - Return: JSON array

POST /api/facts/import
  - Import facts from JSON
  - Body: [{key, value}]
  - Return: {imported: count}
```

### 4. Email Integration (Direct API)
**Required for:**
- Email quick view panel
- Unread count badge
- Email list without going through chat

**Missing Endpoints:**
```python
GET /api/emails
  - Get recent emails (direct API, not via agent)
  - Query params: limit=10, folder=inbox
  - Return: [{id, subject, from, receivedDateTime, isRead, snippet}]
  - Requires M365 authentication

GET /api/emails/unread-count
  - Get unread email count
  - Return: {count: int}

GET /api/m365/status
  - Check M365 connection status
  - Return: {connected: bool, last_sync: datetime, expires_at: datetime}
```

### 5. Calendar Integration (Direct API)
**Required for:**
- Calendar quick view panel
- Upcoming events list
- Event details

**Missing Endpoints:**
```python
GET /api/calendar/events
  - Get calendar events (direct API, not via agent)
  - Query params: days=7, start_date=YYYY-MM-DD
  - Return: [{id, subject, start, end, location, attendees, isAllDay}]
  - Requires M365 authentication

GET /api/calendar/upcoming
  - Get next N upcoming events
  - Query params: limit=5
  - Return: Array of events
```

### 6. Usage Statistics
**Required for:**
- Usage statistics dashboard
- Metrics display

**Missing Endpoints:**
```python
GET /api/stats
  - Get user usage statistics
  - Return: {
      total_messages: int,
      total_conversations: int,
      documents_uploaded: int,
      facts_stored: int,
      api_calls: int,
      usage_by_date: [{date, count}]
    }
  - Filter by user_id
```

### 7. Session Management
**Required for:**
- Better session handling
- Session metadata

**Missing Endpoints:**
```python
GET /api/sessions
  - List all sessions for user
  - Return: [{session_id, created_at, last_activity, message_count}]

PUT /api/conversations/{session_id}/title
  - Update conversation title
  - Body: {title: str}
  - Return: {session_id, title}
```

---

## 🔧 Implementation Priority

### High Priority (Core UI Features)
1. **GET /api/conversations** - Essential for chat history sidebar
2. **GET /api/documents** - Essential for documents manager
3. **GET /api/facts** - Essential for memory panel
4. **GET /api/m365/status** - Essential for connection status

### Medium Priority (Enhanced Features)
5. **GET /api/emails** - For email quick view
6. **GET /api/calendar/events** - For calendar quick view
7. **DELETE /api/conversations/{session_id}** - For conversation management
8. **DELETE /api/documents/{filename}** - For document management
9. **POST/PUT/DELETE /api/facts** - For facts CRUD

### Low Priority (Nice to Have)
10. **GET /api/stats** - For usage dashboard
11. **GET /api/conversations/{session_id}/export** - For export feature
12. **PUT /api/conversations/{session_id}/title** - For editing titles

---

## 📝 Database Considerations

### Current Models (✅ Already Exist)
- `User` - User accounts
- `ChatMessage` - Chat messages
- `UserFact` - User facts/memory

### Potential New Models (If Needed)
```python
# Optional: For better conversation management
class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True)
    session_id = Column(String, unique=True, index=True)
    user_id = Column(Integer, index=True, nullable=True)
    title = Column(String, nullable=True)  # Auto-generated or user-set
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_activity = Column(DateTime(timezone=True))
    message_count = Column(Integer, default=0)
    is_pinned = Column(Boolean, default=False)

# Optional: For document tracking
class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True, nullable=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer)
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="processing")  # processing, ready, error
    indexed = Column(Boolean, default=False)
```

---

## 🚀 Quick Implementation Guide

### Step 1: Create New API Router Files
```
src/api/
├── conversations.py    # New - Conversation management
├── documents.py        # Extend - Add GET, DELETE
├── facts.py            # New - Facts CRUD
├── email.py            # New - Email direct API
├── calendar.py         # New - Calendar direct API
└── stats.py            # New - Usage statistics
```

### Step 2: Add to main.py
```python
from .api import (
    conversations_router,  # New
    facts_router,          # New
    email_router,         # New
    calendar_router,      # New
    stats_router,         # New
)

app.include_router(conversations_router)
app.include_router(facts_router)
app.include_router(email_router)
app.include_router(calendar_router)
app.include_router(stats_router)
```

### Step 3: Reuse Existing Tools
- For email/calendar endpoints, reuse `m365_tools` functions but wrap them in API endpoints
- For facts endpoints, reuse `memory_tools` but add direct database access
- For documents, track uploads in database (optional Document model)

---

## ✅ Summary

**Backend Readiness: ~60%**

**What Works:**
- Core chat functionality ✅
- Authentication ✅
- Voice features ✅
- Document upload ✅
- All tools available via agent ✅

**What's Missing:**
- Direct API endpoints for UI data fetching
- CRUD operations for conversations, documents, facts
- Email/Calendar direct APIs (not just via agent)
- Usage statistics
- Export functionality

**Recommendation:**
The backend has all the **functionality** needed, but needs **additional API endpoints** to support the UI features. The tools exist, they just need to be exposed as REST APIs for direct access from the frontend.

**Estimated Work:**
- High priority endpoints: 2-3 days
- All endpoints: 4-5 days
- With database migrations: 5-7 days


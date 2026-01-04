# Changelog

All notable changes to Project VICTUS will be documented in this file.

## [2.0.0] - 2025-01-XX

### Added
- **OpenAI Integration**: Replaced Google Gemini with OpenAI GPT-4o
- **Modular Tools Architecture**: Refactored tools into organized modules
  - `tools/web_search.py` - Web search functionality
  - `tools/rag_tools.py` - Document querying and RAG
  - `tools/system_tools.py` - System operations
  - `tools/m365_tools.py` - Microsoft 365 integration
  - `tools/weather_tool.py` - Weather information
  - `tools/memory_tools.py` - Long-term memory
  - `tools/assembler.py` - Tool assembly
- **Security Features**:
  - Rate limiting with SlowAPI
  - CORS middleware configuration
  - Input validation and sanitization
  - Session ID validation
- **Logging System**:
  - Structured logging with file and console output
  - Configurable log levels
  - Request/error tracking
- **Testing Framework**:
  - pytest setup with test suite
  - Unit tests for tools
  - API endpoint tests
- **Frontend Improvements**:
  - Modern, responsive UI design
  - Real-time streaming support
  - Better error handling
  - Voice input/output integration
- **Configuration Management**:
  - Centralized settings with Pydantic
  - Environment variable validation
  - Startup configuration checks
- **Error Handling**:
  - Comprehensive exception handling
  - User-friendly error messages
  - Detailed logging for debugging

### Changed
- **Package Structure**: Moved to `src/` directory with proper package structure
- **Import System**: Updated all imports to use package structure
- **Database Models**: Improved type hints and documentation
- **Agent Configuration**: Updated prompts and tool selection logic
- **Dependencies**: Updated to latest versions, replaced Google dependencies with OpenAI

### Fixed
- Import structure issues
- Hardcoded user IDs (now dynamic)
- Missing frontend files
- Error handling in tool execution
- Database session management

### Security
- Added input validation to prevent injection attacks
- Implemented rate limiting to prevent abuse
- Added CORS configuration
- Improved error messages (no sensitive data leakage)

## [1.0.0] - Initial Release

### Features
- Basic AI assistant with Gemini
- Voice I/O support
- Document upload and RAG
- Microsoft 365 integration
- System tools
- Basic chat interface


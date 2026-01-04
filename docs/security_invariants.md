# VICTUS Backend Security Invariants

This document defines the core security model, trust boundaries, and invariants that must be maintained throughout the codebase.

## 1. Trust Boundaries

- **Untrusted**:

  - The Browser Client (Victus Frontend): Can be manipulated by the user or malicious scripts.
  - The Voice WebSocket: Can send arbitrary audio or control messages.
  - File Uploads: Can contain malware or be malformed.
  - External Tool Responses: Can be malicious (e.g. prompt injection from a fetched webpage).

- **Trusted**:
  - The Backend API (Python/FastAPI): Enforces all business logic and invariants.
  - The Database (Postgres): Stores state, secrets (encrypted), and audit logs.
  - The Tool Runtime (Sandbox): Executes tools with strictly defined capabilities.

## 2. Threat Model

| Threat                       | Mitigation                                                                                    |
| :--------------------------- | :-------------------------------------------------------------------------------------------- |
| **IDOR / Session Hijacking** | Strict user-scoping on all DB queries. HttpOnly/Secure cookies. Session revocation.           |
| **Prompt Injection**         | Tool outputs are treated as untrusted data. Human-in-the-loop (HITL) for high-stakes actions. |
| **SSRF**                     | Network fetching tools must block private IP ranges (127.0.0.0/8, 169.254.0.0/16, etc.).      |
| **Tool Abuse**               | Scopes limit available tools per user. Rate limits prevent spam/DoS.                          |
| **Malicious File Upload**    | Strict MIME/Extension allowlist. Filenames randomized (UUID). Files stored outside web root.  |
| **Data Exfiltration**        | Sensitive secrets encrypted at rest. Audit logs track data access.                            |

## 3. Security Invariants (MUST ALWAYS HOLD)

### I1. User Isolation (No Cross-User Access)

Every database query involving user data MUST include a `user_id` filter derived from the authenticated session. There are NO exceptions for "admin" views in the standard API (admin views must be separate/explicit).

### I2. Tool Execution via Runtime & Policy Only

Tools MUST NEVER be executed directly by API endpoints based on raw user input.

1. The LLM proposes a tool call.
2. The `ToolRuntime` checks basic Scopes (`SCOPE_MISSING` if failed).
3. The `PolicyEngine` checks Policy (`POLICY_VIOLATION` if failed or `PENDING_CONFIRMATION`).
4. Only if allowed, the tool executes.

### I3. Confirmations Cannot be Bypassed

If a tool action requires confirmation (Risk Level HIGH or Policy rule), the backend MUST halt execution and wait for an explicit "confirm" intent from the user. The client cannot force execution by setting a flag.

### I4. Zero-Trust Secrets

- API Tokens, OAuth Refresh Tokens, and SMTP Credentials MUST be stored encrypted ($crypto.encrypt_json).
- Secrets MUST NEVER be returned in API responses (redact or omit).
- Secrets MUST NEVER represent raw arguments in logs.

### I5. Ephemeral Audio

Raw audio streams processed by the Voice module MUST NOT be persisted to disk or database by default. Debugging captures must be explicitly strictly opt-in and temporary.

### I6. Safe File Handling

- Input: Max size enforced. Extension verified.
- Storage: Saved as `<UUID>.<ext>`. Original filename stored in DB metadata only.
- Output: Served with `Content-Disposition: attachment` and `X-Content-Type-Options: nosniff`.

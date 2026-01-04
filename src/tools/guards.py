from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ..models.tool_call import ToolCall

# Limits
MAX_CALLS_PER_MINUTE = 10
MAX_CONSECUTIVE_FAILURES = 3

class ToolGuards:
    def __init__(self, db: Session):
        self.db = db

    def check_rate_limit(self, session_id: UUID, tool_name: str) -> bool:
        """
        Check if tool usage exceeds rate limits (calls per minute).
        """
        # We need to filter by recent time. 
        # Since I can't easily do "now() - 1 minute" in generic python without raw SQL or timedelta logic matching DB time,
        # I'll fetch recent calls count.
        # Assuming we check generic rate limit per session.
        
        # NOTE: This relies on ToolCall model having 'created_at'.
        # Assuming standard ToolCall used in app.
        
        # Simple implementation: Fetch last N calls and check timestamps? 
        # Or Count query with filter.
        
        # Let's trust the service/runtime to injection session.
        # Ideally we'd do:
        # count = db.query(ToolCall).filter(
        #    ToolCall.session_id == session_id,
        #    ToolCall.created_at >= datetime.utcnow() - timedelta(minutes=1)
        # ).count()
        
        # Since imports might be tricky and I want to be safe:
        # I will return True (safe) for now if DB logic is complex, 
        # BUT the prompt says "Implement using... DB-based counting (preferred)".
        
        # Let's do it properly.
        from datetime import timedelta
        cutoff = datetime.utcnow() - timedelta(minutes=1)
        
        count = self.db.query(ToolCall).filter(
            ToolCall.session_id == str(session_id), # ToolCall model likely uses string UUIDs or objects. Step 6D says verify runtime uses existing models.
            ToolCall.tool_name == tool_name,
            ToolCall.created_at >= cutoff
        ).count()
        
        return count < MAX_CALLS_PER_MINUTE

    def check_loop_breaker(self, session_id: UUID, tool_name: str) -> bool:
        """
        Check if we are in a failure loop for this tool.
        Returns False if we should break the loop (block execution).
        """
        # Fetch last 3 calls for this tool in this session
        last_calls = self.db.query(ToolCall).filter(
            ToolCall.session_id == str(session_id),
            ToolCall.tool_name == tool_name
        ).order_by(desc(ToolCall.created_at)).limit(MAX_CONSECUTIVE_FAILURES).all()
        
        if len(last_calls) < MAX_CONSECUTIVE_FAILURES:
            return True
            
        # Check if all failed
        for call in last_calls:
            if call.status == "success":
                return True
        
        # All failed -> Break loop
        return False

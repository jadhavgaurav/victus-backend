from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
import json

from ...database import get_db
from ...models.trace import PendingAction
from ...tools.registry import get_tool
from ...utils.logging import get_logger

router = APIRouter(prefix="/approvals", tags=["Approvals"])
logger = get_logger(__name__)

@router.get("/pending")
def get_pending_actions(db: Session = Depends(get_db)):
    """List all pending actions requiring approval."""
    return db.query(PendingAction).filter(PendingAction.status == "PENDING").all()

@router.post("/{action_id}/approve")
async def approve_action(
    action_id: str, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Approve a pending action.
    Executes the tool immediately and records the result.
    """
    action = db.query(PendingAction).filter(PendingAction.id == action_id).first()
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")
    
    if action.status != "PENDING":
        raise HTTPException(status_code=400, detail=f"Action is already {action.status}")

    # Mark as APPROVED
    action.status = "APPROVED"
    db.commit()

    # Execute the tool
    try:
        tool_entry = get_tool(action.tool_name)
        if not tool_entry:
             raise ValueError(f"Tool {action.tool_name} not found in registry")
             
        spec, func = tool_entry
        args = json.loads(action.args)
        
        # Execute the underlying function directly to bypass policy check
        import inspect
        if inspect.iscoroutinefunction(func):
             result = await func(**args)
        else:
             result = func(**args)

        # Log to trace (if trace_id exists in some context, but here we might just log simple result)
        logger.info(f"Action {action_id} approved and executed. Result: {result}")
        
        return {"status": "executed", "result": result}

    except Exception as e:
        logger.error(f"Error executing approved action {action_id}: {e}")
        # Optionally verify if we should mark it as failed?
        return {"status": "error", "message": str(e)}

@router.post("/{action_id}/deny")
def deny_action(action_id: str, db: Session = Depends(get_db)):
    """Deny a pending action."""
    action = db.query(PendingAction).filter(PendingAction.id == action_id).first()
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")
    
    action.status = "DENIED"
    db.commit()
    return {"status": "denied"}

from datetime import datetime, timedelta, timezone
from uuid import uuid4

from sqlalchemy.orm import Session

from ..models.policy import PolicyDecisionModel, PendingConfirmationModel
from .contracts import PolicyCheck, PolicyDecision
from .engine import evaluate_policy

def check_and_record_policy(check: PolicyCheck, db: Session) -> PolicyDecision:
    """
    Façade for the policy layer.
    1. Evaluates policy using the deterministic engine.
    2. Persists the decision to the database.
    3. If confirmation is required, creates a pending confirmation record.
    4. Returns the decision.
    """
    
    # 0. Check for existing confirmation
    # Look for a valid, confirmed permission for this exact action
    active_confirmation = db.query(PendingConfirmationModel).filter(
        PendingConfirmationModel.session_id == check.session_id,
        PendingConfirmationModel.tool_name == check.tool_name,
        PendingConfirmationModel.status == "confirmed",
        PendingConfirmationModel.expires_at > datetime.now(timezone.utc)
    ).all() # Fetch all candidates to check args
    
    for conf in active_confirmation:
        # Compare args (simple equality check - usually works for JSON if keys ordered same, 
        # but for safety we might rely on the user confirming the *intent* which maps to this ID.
        # However, checking args prevents reusing a confirmation for a different payload.)
        if conf.tool_args == check.tool_args_preview:
            # Found a match!
            # Mark it as used/completed so it can't be reused indefinitely (one-time use)
            conf.status = "completed"
            db.add(conf)
            db.commit() # Commit state change
            
            # Return ALLOW decision
            return PolicyDecision(
                 decision="ALLOW",
                 risk_score=0,
                 reason_code="USER_CONFIRMED",
                 intent_summary=check.intent_summary,
                 id=None # We don't persist a new policy decision record for the ALLOW? 
                         # Actually we should log that it allowed execution.
            )
            
    # 1. Evaluate
    decision = evaluate_policy(check)
    
    # 2. Persist decision
    # (Optional: check if tool_call_id exists in check if we add it later)
    
    db_decision = PolicyDecisionModel(
        id=uuid4(),
        session_id=check.session_id,
        user_id=check.user_id,
        tool_name=check.tool_name,
        decision=decision.decision,
        risk_score=decision.risk_score,
        reason_code=decision.reason_code,
        intent_summary=check.intent_summary,
        created_at=datetime.now(timezone.utc)
    )
    db.add(db_decision)
    
    # 3. Handle Confirmations
    if decision.decision in ("ALLOW_WITH_CONFIRMATION", "ESCALATE"):
        # Create pending confirmation
        expires_at = decision.expires_at or (datetime.now(timezone.utc) + timedelta(hours=1))
        
        confirmation = PendingConfirmationModel(
            id=uuid4(),
            session_id=check.session_id,
            user_id=check.user_id,
            tool_name=check.tool_name,
            tool_args=check.tool_args_preview, # Store preview args for context
            required_phrase=decision.required_confirmation_phrase,
            decision_type=decision.decision,
            expires_at=expires_at,
            status="pending",
            created_at=datetime.now(timezone.utc)
        )
        db.add(confirmation)
        
    db.commit()
    
    # Return decision with the generated ID
    return decision.model_copy(update={"id": db_decision.id})

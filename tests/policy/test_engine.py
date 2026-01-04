from uuid import uuid4
from src.policy.contracts import PolicyCheck
from src.policy.engine import evaluate_policy

def create_check(tool_name, action_type="READ", **kwargs):
    defaults = {
        "user_id": uuid4(),
        "session_id": uuid4(),
        "target_entity": "test_entity",
        "scope": "single",
        "sensitivity": "low",
        "intent_summary": "Test intent",
        "tool_args_preview": {"arg": "val"},
    }
    defaults.update(kwargs)
    
    return PolicyCheck(
        tool_name=tool_name,
        action_type=action_type,
        **defaults
    )

def test_unknown_tool_deny():
    check = create_check(tool_name="unknown.tool")
    decision = evaluate_policy(check)
    assert decision.decision == "DENY"
    assert decision.reason_code == "UNKNOWN_TOOL"
    assert decision.risk_score == 100

def test_readonly_low_risk_allow():
    # calendar.read is low risk, read only, no side effects
    check = create_check("calendar.read", action_type="READ", sensitivity="low")
    decision = evaluate_policy(check)
    assert decision.decision == "ALLOW"
    assert decision.risk_score <= 10
    assert decision.reason_code == "LOW_RISK_READ"

def test_external_communication_confirm():
    # email.send is external comms
    check = create_check("email.send", action_type="WRITE", sensitivity="high")
    decision = evaluate_policy(check)
    assert decision.decision == "ALLOW_WITH_CONFIRMATION"
    assert decision.risk_score >= 60
    assert "external" in decision.user_prompt or "communicate" in decision.user_prompt
    assert decision.reason_code == "EXTERNAL_COMM_CONFIRM"

def test_destructive_escalate():
    # file.delete is destructive
    check = create_check("file.delete", action_type="DELETE", sensitivity="high")
    decision = evaluate_policy(check)
    assert decision.decision == "ESCALATE"
    assert decision.risk_score >= 85
    assert decision.required_confirmation_phrase is not None
    assert "DELETE" in decision.required_confirmation_phrase

def test_batch_scope_increases_risk_and_confirms():
    # email.read is medium sensitivity. Batch should bump it up.
    check = create_check("email.read", action_type="READ", scope="batch", sensitivity="medium")
    decision = evaluate_policy(check)
    
    # Logic: Base medium (40) + Batch (20) = 60.
    # Rule 5: If batch and decision==ALLOW and risk > 30 -> ALLOW_WITH_CONFIRMATION.
    # Base decision for email.read? default_action=READ, side_effects=False.
    # But sensitivity is medium. 
    # Rule 2 (ALLOW) only applies if sensitivity=low.
    # So initial decision falls through to ALLOW logic?
    # Engine logic:
    # default decision = ALLOW.
    # risk = 40 + 20 = 60.
    # Rule 5: is_batch and decision==ALLOW ("ALLOW") and risk > 30 (60) -> ALLOW_WITH_CONFIRMATION.
    
    assert decision.decision == "ALLOW_WITH_CONFIRMATION"
    assert decision.risk_score >= 60
    assert decision.reason_code == "BATCH_OPERATION_CONFIRM"

def test_system_exec_escalate():
    # system.clock is system category, but usually read.
    # We force check inputs to match logic for system execution if tool existed,
    # or modify registry mock?
    # But we check registry: system.clock default is READ.
    # If we request EXECUTE action on system.clock:
    # Tool registry says default is READ, side_effects=False.
    # Check says action=EXECUTE.
    # Engine logic checks: is_system_exec = category=="system" and action=="EXECUTE".
    
    check = create_check("system.clock", action_type="EXECUTE")
    decision = evaluate_policy(check)
    assert decision.decision == "ESCALATE"
    assert decision.risk_score == 100
    assert decision.required_confirmation_phrase == "CONFIRM SYSTEM EXECUTE"

def test_risk_normalization():
    # Ensure score never exceeds 100 or drops below 0
    # Use a fake tool logic test or just boundary checks.
    # file.delete is sensitive (high=70) + destructive (85 min).
    check = create_check("file.delete", action_type="DELETE", sensitivity="high")
    decision = evaluate_policy(check)
    assert 0 <= decision.risk_score <= 100

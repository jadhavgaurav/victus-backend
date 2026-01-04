from prometheus_client import Counter, Histogram, Gauge, REGISTRY

# Helper to avoid duplication on reload
def get_or_create_metric(metric_type, name, documentation, labels=None, **kwargs):
    if name in REGISTRY._names_to_collectors:
        return REGISTRY._names_to_collectors[name]
    if labels:
        return metric_type(name, documentation, labels, **kwargs)
    return metric_type(name, documentation, **kwargs)

# General Request Metrics
REQUESTS_TOTAL = get_or_create_metric(
    Counter,
    "victus_requests_total", 
    "Total number of requests", 
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = get_or_create_metric(
    Histogram,
    "victus_request_latency_ms",
    "Request latency in milliseconds",
    ["method", "endpoint"]
)

# Tool Metrics
TOOL_CALLS_TOTAL = get_or_create_metric(
    Counter,
    "victus_tool_calls_total",
    "Total tool executions",
    ["tool_name", "status"]
)

TOOL_ERRORS_TOTAL = get_or_create_metric(
    Counter,
    "victus_tool_errors_total",
    "Total tool execution errors",
    ["tool_name", "error_type"]
)

# Policy Metrics
POLICY_DENIES_TOTAL = get_or_create_metric(
    Counter,
    "victus_policy_denies_total",
    "Total policy denials",
    ["tool_name", "reason"]
)

CONFIRMATIONS_PENDING = get_or_create_metric(
    Gauge,
    "victus_confirmations_pending",
    "Current number of pending confirmations"
)

# WS Metrics
WS_CONNECTIONS_ACTIVE = get_or_create_metric(
    Gauge,
    "victus_ws_connections_active",
    "Number of active WebSocket connections"
)

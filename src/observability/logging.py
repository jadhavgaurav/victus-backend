import sys
import json
import logging
from opentelemetry import trace

class JsonFormatter(logging.Formatter):
    def format(self, record):
        span_context = trace.get_current_span().get_span_context()
        trace_id = f"{span_context.trace_id:032x}" if span_context.is_valid else None
        span_id = f"{span_context.span_id:016x}" if span_context.is_valid else None
        
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "trace_id": trace_id,
            "span_id": span_id,
        }
        
        # Add extra fields if present
        if hasattr(record, "user_id"):
            log_record["user_id"] = record.user_id
        if hasattr(record, "session_id"):
            log_record["session_id"] = record.session_id
            
        return json.dumps(log_record)

def configure_logging(level=logging.INFO):
    """
    Configure root logger to output JSON to stdout.
    """
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Remove existing handlers to avoid double logging
    for h in root_logger.handlers[:]:
        root_logger.removeHandler(h)
        
    root_logger.addHandler(handler)
    
    # Silence noisy libs
    logging.getLogger("uvicorn.access").disabled = True # We use our own middleware logs usually

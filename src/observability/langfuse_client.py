import os
from typing import Dict, Any
from langfuse import Langfuse

from ..utils.logging import get_logger

logger = get_logger(__name__)

class LangfuseWrapper:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LangfuseWrapper, cls).__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        self.enabled = False
        try:
            public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
            secret_key = os.getenv("LANGFUSE_SECRET_KEY")
            
            if public_key and secret_key:
                self.client = Langfuse(
                    public_key=public_key,
                    secret_key=secret_key,
                    host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
                )
                self.enabled = True
                logger.info("Langfuse client initialized.")
            else:
                self.client = None
                logger.warning("Langfuse credentials not found. Tracing disabled.")
        except Exception as e:
            logger.error(f"Error initializing Langfuse: {e}")
            self.client = None

    def trace(self, name: str, user_id: str = None, session_id: str = None, **kwargs):
        """Start a new Langfuse trace."""
        if not self.enabled or not self.client:
            return None
        
        try:
            return self.client.trace(
                name=name,
                user_id=user_id,
                session_id=session_id,
                **kwargs
            )
        except Exception as e:
            logger.error(f"Langfuse trace error: {e}")
            return None

    def observe(self, trace_obj, name: str, input: Any, output: Any = None, metadata: Dict = None, level: str = None):
        """Add an observation (span/generation) to a trace."""
        if not trace_obj:
            return

        try:
            # We treat generic observations as spans unless specified otherwise
            # In Langfuse, 'span' is generic unit of work.
            trace_obj.span(
                name=name,
                input=input,
                output=output,
                metadata=metadata,
                level=level
            )
        except Exception as e:
            logger.error(f"Langfuse observation error: {e}")

    def flush(self):
        if self.enabled and self.client:
            self.client.flush()

langfuse_client = LangfuseWrapper()

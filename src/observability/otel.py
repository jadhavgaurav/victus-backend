import os

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
# If using HTTP: from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

from ..config import settings
from ..utils.logging import get_logger

logger = get_logger(__name__)

def setup_opentelemetry(app):
    """
    Bootstrap OpenTelemetry and configure exporters.
    """
    resource = Resource.create(attributes={
        "service.name": settings.PROJECT_NAME,
        "service.version": settings.PROJECT_VERSION,
        "deployment.environment": settings.ENVIRONMENT,
    })

    provider = TracerProvider(resource=resource)
    
    # Configure OTLP Exporter (Langfuse / Tempo)
    # Langfuse typically expects: OTEL_EXPORTER_OTLP_ENDPOINT
    # We check env or config.
    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    
    if endpoint:
        try:
            exporter = OTLPSpanExporter(endpoint=endpoint)
            span_processor = BatchSpanProcessor(exporter)
            provider.add_span_processor(span_processor)
            logger.info(f"OpenTelemetry enabled. Exporter: {endpoint}")
        except Exception as e:
            logger.error(f"Failed to initialize OTLP exporter: {e}")
    else:
        logger.warning("OTEL_EXPORTER_OTLP_ENDPOINT not set. Traces will not be exported.")

    # Set global provider
    trace.set_tracer_provider(provider)

    # Instrument Libraries
    FastAPIInstrumentor.instrument_app(app, tracer_provider=provider)
    RequestsInstrumentor().instrument(tracer_provider=provider)
    
    # SQLAlchemy instrumentation requires engine. 
    # Usually handled where engine is created, or instrument globally (might catch all engines)
    # SQLAlchemyInstrumentor().instrument(
    #     tracer_provider=provider,
    #     engine=engine # optional if you want specific engine
    # )
    
    return provider

def get_tracer(name: str):
    return trace.get_tracer(name)

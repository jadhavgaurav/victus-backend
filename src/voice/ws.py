import json
import base64
import traceback

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from pydantic import ValidationError

from ..utils.logging import get_logger
from ..database import get_db
from ..models import User
from ..models.conversation import Conversation
from ..models.message import Message

from ..agent.orchestrator import AgentOrchestrator
from ..services.voice import VoiceService

from .contracts import (
    WakeEvent, AudioChunk, EndOfUtterance, TranscriptFinal, AssistantResponse, TTSChunk, ErrorEvent
)

# Note: We'll likely need to import STT/TTS adapters if we split them out. 
# For MVP, we can re-use VoiceService directly in the loop.

logger = get_logger(__name__)
router = APIRouter(prefix="/ws", tags=["Voice"])

# We should ideally rely on a ConnectionManager if scaling, but for single instance MVP:
class VoiceSession:
    def __init__(self, ws: WebSocket, user: User, db_session):
        self.ws = ws
        self.user = user
        self.db = db_session
        self.active = True
        self.listening = False
        self.audio_buffer = bytearray()
        
        # Tools
        self.voice_service = VoiceService() # Re-init or singleton? Singleton preferred usually.
        self.orchestrator = AgentOrchestrator()
        
    async def send_json(self, model):
        try:
            await self.ws.send_json(model.model_dump())
        except Exception as e:
            logger.error(f"Error sending WS: {e}")

    async def handle_wake(self, event: WakeEvent):
        logger.info(f"Wake detected: {event.wake_word}")
        self.listening = True
        self.audio_buffer = bytearray()
        # Create or retrieve conversation session
        # We can key off session_id from client or create new.
        # For this MVP, we treat each Wake as start of turn in a persistent session?
        pass

    async def handle_audio(self, event: AudioChunk):
        if not self.listening:
            return
            
        try:
            data = base64.b64decode(event.chunk_b64)
            self.audio_buffer.extend(data)
            
            # Streaming STT would go here.
            # For MVP buffered: we just accumulate.
        except Exception as e:
            logger.error(f"Audio decode fail: {e}")

    async def handle_eou(self, event: EndOfUtterance):
        logger.info("End of utterance received. Processing...")
        self.listening = False
        
        # 1. Transcribe
        transcript = self.voice_service.transcribe(bytes(self.audio_buffer))
        logger.info(f"Transcript: {transcript}")
        
        # Observation: STT
        if hasattr(self, 'current_trace') and self.current_trace:
             from ..observability.langfuse_client import langfuse_client
             langfuse_client.observe(
                 self.current_trace,
                 "voice.transcription",
                 input={"audio_bytes_length": len(self.audio_buffer)},
                 output=transcript
             )
        
        await self.send_json(TranscriptFinal(text=transcript, confidence=1.0))
        
        if not transcript.strip():
            return

        # 2. Orchestrate
        session_id = None 
        # Hacky session lookup for MVP
        conv = self.db.query(Conversation).filter(
            Conversation.user_id == self.user.id
        ).order_by(Conversation.updated_at.desc()).first()
        
        if not conv:
            conv = Conversation(user_id=self.user.id, title="Voice Session")
            self.db.add(conv)
            self.db.commit()
            
        session_id = conv.id
        self.db_session_id = session_id # Store for trace context update if needed

        # We pass the trace_id in metadata or context so orchestrator can use it?
        # Ideally Orchestrator manages its own trace or becomes a child span.
        # For simplicity, we assume Orchestrator starts 'victus.command' trace.
        # But here 'voice.wake' is the parent trace.
        # Langfuse nesting requires creating a span manually or passing trace obj.
        # We can let Orchestrator start a new trace 'victus.command' independently for now, 
        # OR better: pass trace_id to orchestrator. 
        # Orchestrator signature doesn't take trace_id. 
        
        orch_resp = self.orchestrator.handle_user_utterance(
            db=self.db,
            user_id=self.user.id,
            session_id=session_id,
            utterance=transcript,
            modality="voice"
        )
        
        resp_text = orch_resp.assistant_text
        await self.send_json(AssistantResponse(text=resp_text))
        
        # 3. TTS
        if orch_resp.should_speak and resp_text:
            audio_bytes = self.voice_service.synthesize(resp_text)
            if audio_bytes:
                b64 = base64.b64encode(audio_bytes).decode('utf-8')
                await self.send_json(TTSChunk(chunk_b64=b64, seq=0))


@router.websocket("/voice")
async def voice_websocket(
    websocket: WebSocket,
    # token: str = Query(...) # Auth integration needed
    db = Depends(get_db)
):
    # Origin Check
    from ..config import settings
    origin = websocket.headers.get("origin")
    if origin and origin not in settings.CORS_ORIGINS:
         # Be strict if origin is present
         await websocket.close(code=4003, reason="Forbidden Origin")
         return
         
    await websocket.accept()
    
    # Mock user auth for MVP if token logic not ready for WS
    # In real app: verify token. 
    # Here lets assume we can get a user from DB or header?
    # WS headers are tricky. Usually sends token in query param.
    # For Step 8 demo, we might need a workaround or just grab first user (Dev).
    from ..models import User
    user = db.query(User).first() # DEV HACK
    
    if not user:
        await websocket.close(code=4001, reason="No user found")
        return

    from ..observability.langfuse_client import langfuse_client
    from ..observability.metrics import WS_CONNECTIONS_ACTIVE
    
    WS_CONNECTIONS_ACTIVE.inc()

    session = VoiceSession(websocket, user, db)
    
    try:
        while True:
            data = await websocket.receive_text()
            try:
                msg = json.loads(data)
                type_ = msg.get("type")
                
                # Trace incoming event
                if type_ == "wake":
                    # Start trace on wake if treating wake as start of interaction
                    # We might want to trace entire session or just the turn.
                    # Let's trace the turn.
                    wake_event = WakeEvent(**msg)
                    trace = langfuse_client.trace(
                        name="voice.wake",
                        user_id=str(user.id),
                        session_id=str(session.db_session_id) if hasattr(session, 'db_session_id') else None,
                        metadata={"wake_word": wake_event.wake_word}
                    )
                    session.current_trace = trace
                    await session.handle_wake(wake_event)
                    
                elif type_ == "audio":
                    await session.handle_audio(AudioChunk(**msg))
                    
                elif type_ == "eou":
                    if hasattr(session, 'current_trace') and session.current_trace:
                         langfuse_client.observe(
                             session.current_trace, 
                             "voice.eou_detected", 
                             input={"timestamp": msg.get("timestamp")}
                         )
                    await session.handle_eou(EndOfUtterance(**msg))
                    
                    # End trace after EOU processing loop?
                    # Ideally handle_eou does all the work.
                    
                elif type_ == "cancel":
                    if hasattr(session, 'current_trace') and session.current_trace:
                        langfuse_client.observe(
                            session.current_trace,
                            "voice.cancelled",
                            input={}
                        )
                    session.listening = False
                    session.audio_buffer = bytearray()
                    
            except ValidationError as e:
                await session.send_json(ErrorEvent(message=f"Validation details: {e}"))
            except Exception as e:
                logger.error(f"Processing error: {e}")
                traceback.print_exc()
                await session.send_json(ErrorEvent(message=str(e)))

    except WebSocketDisconnect:
        logger.info("Voice WS Disconnected")
    finally:
        WS_CONNECTIONS_ACTIVE.dec()

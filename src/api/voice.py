import base64
import asyncio
from fastapi import APIRouter, Request, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session

from ..utils.logging import get_logger
from ..database import get_db
from ..auth.dependencies import get_current_user
from ..services.voice import VoiceService
from ..agent.orchestrator import AgentOrchestrator

logger = get_logger(__name__)
router = APIRouter(prefix="/api/voice", tags=["Voice"])

# We can instantiate service globally or via dependency. 
# Global is easier for caching connections.
voice_service = VoiceService()

@router.post("/chat")
async def voice_chat(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    # Optional: conversation_id form field if needed, but for now assuming new or infer
):
    """
    Full Voice-to-Voice Loop:
    Audio -> STT -> Orchestrator -> TTS -> Audio
    """
    try:
        # 1. Transcribe
        audio_bytes = await file.read()
        transcript = await asyncio.to_thread(voice_service.transcribe, audio_bytes)
        logger.info(f"Transcript: {transcript}")
        
        if not transcript:
             return JSONResponse({"text": "", "audio": None})

        # 2. Orchestrate
        orchestrator = AgentOrchestrator()
        
        # We need a proper session ID. 
        # For this endpoint, let's look up or create a default session/conversation for the user?
        # Or simple: Use the user's ID as session for stateless voice commands, 
        # but Orchestrator expects UUID session linked to session table.
        # Let's verify if we have a way to get 'current' session or just pick latest.
        
        # Quick fix: Use a specific "Voice Session" or find latest active session.
        # For Step 8, let's create a new session if none provided, but we don't have conv_id in params.
        # Ideally, voice chat should accept conversation_id.
        # I'll default to looking up the most recent conversation or creating one.
        
        from ..models.conversation import Conversation
        conversation = db.query(Conversation).filter(
            Conversation.user_id == current_user.id
        ).order_by(Conversation.updated_at.desc()).first()
        
        if not conversation:
             conversation = Conversation(user_id=current_user.id, title="Voice Chat")
             db.add(conversation)
             db.commit()
             
        session_id = conversation.id
        
        # Execute Intent
        # We run this in thread pool to avoid blocking async event loop
        response = await asyncio.to_thread(
            orchestrator.handle_user_utterance,
            db=db,
            user_id=current_user.id,
            session_id=session_id, # Using conversation_id as session_id
            utterance=transcript,
            modality="voice"
        )
        
        response_text = response.assistant_text
        
        # 3. Synthesize
        audio_out = None
        if response_text and response.should_speak:
            audio_out_bytes = await asyncio.to_thread(voice_service.synthesize, response_text)
            if audio_out_bytes:
                 audio_out = base64.b64encode(audio_out_bytes).decode('utf-8')
        
        return JSONResponse({
            "user_transcript": transcript,
            "assistant_text": response_text,
            "audio_base64": audio_out,
            "tool_result": response.metadata.get("tool_result") if response.metadata else None
        })

    except Exception as e:
        logger.error(f"Voice Chat Error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Voice processing failed: {str(e)}"
        )

@router.post("/transcribe")
async def transcribe_only(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    text = await asyncio.to_thread(voice_service.transcribe, audio_bytes)
    return {"text": text}

@router.post("/synthesize")
async def synthesize_only(request: Request):
    body = await request.json()
    text = body.get("text")
    if not text:
         raise HTTPException(400, "Missing text")
         
    audio_bytes = await asyncio.to_thread(voice_service.synthesize, text)
    
    # Return as streaming response or blob? 
    # For now, base64 JSON or raw bytes. Raw bytes is standard.
    return Response(content=audio_bytes, media_type="audio/mpeg")

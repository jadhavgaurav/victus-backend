from typing import Optional, Literal
from pydantic import BaseModel

class VoiceEventBase(BaseModel):
    type: str
    session_id: str
    user_id: str

# --- Client -> Server Events ---

class WakeEvent(VoiceEventBase):
    type: Literal["wake"] = "wake"
    wake_word: str
    timestamp: float

class AudioChunk(VoiceEventBase):
    type: Literal["audio"] = "audio"
    chunk_b64: str  # Base64 encoded PCM/WAV
    sample_rate: int = 16000
    channels: int = 1
    seq: int  # Sequence number

class EndOfUtterance(VoiceEventBase):
    type: Literal["eou"] = "eou"
    timestamp: float

class CancelEvent(VoiceEventBase):
    type: Literal["cancel"] = "cancel"

# --- Server -> Client Events ---

class TranscriptPartial(BaseModel):
    type: Literal["transcript_partial"] = "transcript_partial"
    text: str

class TranscriptFinal(BaseModel):
    type: Literal["transcript_final"] = "transcript_final"
    text: str
    confidence: Optional[float] = None
    mic_id: Optional[str] = None # Or any tracing ID

class AssistantResponse(BaseModel):
    type: Literal["assistant_response"] = "assistant_response"
    text: str

class TTSChunk(BaseModel):
    type: Literal["tts_chunk"] = "tts_chunk"
    chunk_b64: str
    seq: int

class ErrorEvent(BaseModel):
    type: Literal["error"] = "error"
    message: str

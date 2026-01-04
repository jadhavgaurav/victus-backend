import io
from openai import OpenAI
from ..utils.logging import get_logger
from ..config import settings

logger = get_logger(__name__)

class VoiceService:
    def __init__(self):
        self.openai_client = None
        self.mode = "openai" # or "local"
        
        # Check for OpenAI Key
        if settings.OPENAI_API_KEY:
            self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
            self.mode = "openai"
            logger.info("VoiceService initialized in OpenAI mode.")
        else:
            self.mode = "local"
            logger.warning("VoiceService initialized in Local mode (OpenAI key not found). Local models might need manual setup.")

    def transcribe(self, audio_bytes: bytes) -> str:
        """
        Transcribe audio bytes to text.
        """
        if self.mode == "openai":
            return self._transcribe_openai(audio_bytes)
        else:
            return self._transcribe_local(audio_bytes)

    def synthesize(self, text: str) -> bytes:
        """
        Synthesize text to audio bytes (MP3/WAV).
        """
        if self.mode == "openai":
            return self._synthesize_openai(text)
        else:
            return self._synthesize_local(text)

    def _transcribe_openai(self, audio_data: bytes) -> str:
        try:
            # OpenAI API requires a file-like object with a name
            audio_file = io.BytesIO(audio_data)
            audio_file.name = "audio.wav"
            
            transcript = self.openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
            return transcript.text
        except Exception as e:
            logger.error(f"OpenAI STT Error: {e}")
            raise

    def _synthesize_openai(self, text: str) -> bytes:
        try:
            response = self.openai_client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=text
            )
            return response.content
        except Exception as e:
            logger.error(f"OpenAI TTS Error: {e}")
            raise

    def _transcribe_local(self, audio_data: bytes) -> str:
        # Placeholder for Faster Whisper
        # Implementing full local stack requires significant model download/setup.
        # For now, we return a mock or raise non-implemented if dependencies missing.
        logger.warning("Local STT not fully implemented in this step. Returning mock.")
        return "Local transcription placeholder."

    def _synthesize_local(self, text: str) -> bytes:
        # Placeholder for Piper TTS
        logger.warning("Local TTS not fully implemented in this step. Returning empty bytes.")
        return b""

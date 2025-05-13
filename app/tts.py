from transformers import pipeline
from app.config import settings

# Initialize TTS pipeline (lazy load)
_tts_pipeline = None

def get_tts_pipeline():
    global _tts_pipeline
    if _tts_pipeline is None:
        _tts_pipeline = pipeline(
            task="text-to-speech",
            model=settings.MODEL_NAME,
            framework="pt",
            device=0
        )
    return _tts_pipeline


def synthesize(text: str, speaker: str = None, **kwargs) -> bytes:
    """
    Generate speech audio bytes (wav).
    Support SSML by passing text with SSML tags.
    """
    tts = get_tts_pipeline()
    output = tts(text, **kwargs)
    # output["audio"] is raw audio array; pipeline returns dict with 'audio'
    return output["audio"]
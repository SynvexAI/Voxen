import io
from fastapi.responses import StreamingResponse

def stream_wav(audio_bytes: bytes, sample_rate: int):
    buffer = io.BytesIO()
    # Write WAV header + PCM
    import soundfile as sf
    sf.write(buffer, audio_bytes, sample_rate, format='WAV')
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="audio/wav")
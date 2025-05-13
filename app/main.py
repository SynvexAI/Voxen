from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.tts import synthesize
from app.config import settings
from app.utils import stream_wav

class TTSRequest(BaseModel):
    text: str
    format: str = "wav"       # wav or mp3
    sample_rate: int = settings.SAMPLE_RATE
    speaker: str = None

app = FastAPI(title="ChatGPT-level TTS Service")

@app.post("/synthesize")
def synthesize_endpoint(req: TTSRequest):
    try:
        audio = synthesize(req.text, speaker=req.speaker)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if req.format == "wav":
        return stream_wav(audio, req.sample_rate)
    else:
        # Convert to mp3 on the fly
        import io, pydub
        buffer = io.BytesIO()
        sound = pydub.AudioSegment(
            audio.tobytes(),
            frame_rate=req.sample_rate,
            sample_width=audio.dtype.itemsize,
            channels=1
        )
        sound.export(buffer, format="mp3")
        buffer.seek(0)
        return StreamingResponse(buffer, media_type="audio/mpeg")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
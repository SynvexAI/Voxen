import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    MODEL_NAME: str = os.getenv("MODEL_NAME", "tts_models/en/ljspeech/tacotron2-DDC")
    SAMPLE_RATE: int = 22050
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    class Config:
        env_file = ".env"

settings = Settings()
# app/main.py
from app.routes.audio import router as audio_router
from fastapi import FastAPI

app = FastAPI()


def create_app() -> FastAPI:
    app = FastAPI(title="Audio Processing API")

    # Registrar el router de audio
    app.include_router(audio_router, prefix="/audio", tags=["audio"])

    return app


app = create_app()

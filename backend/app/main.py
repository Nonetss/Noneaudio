# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.audio import router as audio_router

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # otros orígenes si hacen falta
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Resto de configuración...


def create_app() -> FastAPI:
    app = FastAPI(title="Audio Processing API")

    # Registrar el router de audio
    app.include_router(audio_router, prefix="/audio", tags=["audio"])

    return app


app = create_app()

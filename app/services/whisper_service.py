# app/services/whisper_service.py
import whisper

# Cargamos el modelo cuando se importa el archivo
whisper_model = whisper.load_model("small")


def transcribe_audio(audio_path: str, language: str = "es") -> str:
    """
    Transcribe el audio utilizando Whisper.
    """
    result = whisper_model.transcribe(audio_path, language=language)
    return result["text"]

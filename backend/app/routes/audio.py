# app/routes/audio.py
from pathlib import Path

from fastapi import APIRouter, File, UploadFile

from app.services.ollama_service import generate_summary_with_ollama
from app.services.whisper_service import transcribe_audio
from app.utils.file_ops import convert_to_wav, create_directories, save_text_to_md

router = APIRouter()

# Carpeta raíz para los archivos
FILES_PATH = Path("app/files")
FILES_PATH.mkdir(parents=True, exist_ok=True)


@router.post("/upload-audio/")
async def upload_audio(file: UploadFile = File(...)):
    # 1. Crear carpetas organizadas por el nombre del archivo (sin extensión)
    audio_name = Path(file.filename).stem
    base_path = FILES_PATH / audio_name
    folders = create_directories(base_path)

    # 2. Guardar el archivo de audio subido temporalmente
    temp_audio_path = base_path / file.filename
    with open(temp_audio_path, "wb") as f:
        f.write(await file.read())

    # 3. Convertir a WAV en la carpeta "audio"
    processed_audio_path = folders["audio"] / f"{audio_name}.wav"
    try:
        convert_to_wav(temp_audio_path, processed_audio_path)
    except Exception as e:
        temp_audio_path.unlink(missing_ok=True)
        return {"error": "Error al convertir el audio a WAV", "details": str(e)}
    finally:
        # Eliminar el archivo original
        temp_audio_path.unlink(missing_ok=True)

    # 4. Transcribir con Whisper
    try:
        transcription = transcribe_audio(str(processed_audio_path), language="es")
    except Exception as e:
        return {"error": "Falló la transcripción con Whisper", "details": str(e)}

    # 5. Guardar la transcripción en un archivo .md
    try:
        transcription_md_path = (
            folders["transcriptions"] / f"{audio_name}_transcription.md"
        )
        save_text_to_md(
            transcription_md_path,
            title=f"Transcripción para {audio_name}",
            content=transcription,
        )
    except Exception as e:
        return {
            "error": "Error al guardar la transcripción en Markdown",
            "details": str(e),
        }

    # 6. Generar el resumen con Ollama
    try:
        summary = generate_summary_with_ollama(transcription)
    except Exception as e:
        return {"error": "Error al generar el resumen con Ollama", "details": str(e)}

    # 7. Guardar el resumen en otro archivo .md
    try:
        summary_md_path = folders["summaries"] / f"{audio_name}_summary.md"
        save_text_to_md(
            summary_md_path, title=f"Resumen para {audio_name}", content=summary
        )
    except Exception as e:
        return {"error": "Error al guardar el resumen en Markdown", "details": str(e)}

    return {
        "message": "Audio procesado exitosamente",
        "processed_audio_path": str(processed_audio_path),
        "transcription_md_path": str(transcription_md_path),
        "summary_md_path": str(summary_md_path),
        "transcription": transcription,
        "summary": summary,
    }

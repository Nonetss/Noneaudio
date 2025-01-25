# app/utils/file_ops.py

import subprocess
from pathlib import Path


def create_directories(base_path: Path) -> dict:
    """
    Crea las carpetas necesarias para organizar los archivos.
    """
    paths = {
        "audio": base_path / "audio",
        "transcriptions": base_path / "transcriptions",
        "summaries": base_path / "summaries",
    }
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    return paths


def convert_to_wav(input_path: Path, output_path: Path) -> None:
    """
    Convierte cualquier archivo de audio al formato WAV utilizando ffmpeg.
    """
    subprocess.run(["ffmpeg", "-i", str(input_path), str(output_path)], check=True)


def save_text_to_md(md_path: Path, title: str, content: str) -> None:
    """
    Guarda texto en un archivo Markdown (.md) con un título y un contenido dado.
    """
    with open(md_path, "w", encoding="utf-8") as md_file:
        md_file.write(f"# {title}\n\n")
        md_file.write(content)

# app/services/ollama_service.py
import ollama


def generate_summary_with_ollama(
    transcription: str, model: str = "llama3.2:latest"
) -> str:
    """
    Genera un resumen estructurado de la transcripción usando Ollama.
    """
    prompt = f"""
    Voy a proporcionarte la transcripción de un audio. No hagas referencia a que es una transcripción,
    tiene que parecer que la nota la haya escrito yo. Dale un título, un resumen de los puntos claves y
    después desarrolla las ideas.
    Aquí está la transcripción del audio:

    {transcription}
    """

    response = ollama.chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    if "message" not in response or "content" not in response["message"]:
        raise ValueError(f"Formato de respuesta inesperado de Ollama: {response}")

    return response["message"]["content"]

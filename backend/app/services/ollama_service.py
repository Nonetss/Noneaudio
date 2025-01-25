from ollama import Client

# Configuración del cliente con la URL del host
client = Client(host="http://host.docker.internal:11434")


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

    # Llamada al modelo de Ollama
    response = client.chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    # Extraer contenido del mensaje
    if not response or not response.message or not response.message.content:
        raise ValueError(f"Formato de respuesta inesperado de Ollama: {response}")

    return response.message.content

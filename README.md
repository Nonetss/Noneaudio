# Audio Processing Application

## Descripción del Proyecto

Este proyecto es una aplicación que permite a los usuarios procesar audios de forma eficiente desde una interfaz web. Los usuarios pueden **subir audios** o **grabar directamente desde su micrófono**, tras lo cual el sistema realiza las siguientes acciones:

1. **Transcripción de Audio**: Convierte el audio en texto utilizando el modelo **Whisper**.
2. **Generación de Resúmenes**: Procesa la transcripción con **Ollama**, un modelo de lenguaje avanzado, para generar un resumen estructurado.
3. **Almacenamiento**: Guarda los archivos de audio, transcripciones y resúmenes en el servidor de manera organizada.

[Imagen frontend](./static/screenshot_26012025_155539.jpg)

## Tecnologías Utilizadas

### **Frontend**

- **React**: Para la construcción de una interfaz de usuario moderna y dinámica.
- **Vite**: Herramienta para un entorno de desarrollo rápido y eficiente.
- **CSS**: Para el diseño responsivo y estilizado de la aplicación.
- **Nginx**: Servidor para servir el frontend en producción.

### **Backend**

- **FastAPI**: Framework de Python para la creación de una API rápida y eficiente.
- **Whisper**: Modelo de transcripción de audio desarrollado por OpenAI.
- **Ollama**: Modelo de lenguaje para generar resúmenes estructurados.
- **Python**: Lenguaje principal para la lógica del backend.

### **DevOps**

- **Docker**: Para empaquetar y desplegar la aplicación en contenedores.
- **Docker Compose**: Para orquestar múltiples servicios como el backend y frontend.
- **Nginx**: Servidor HTTP para distribuir el frontend.

## ¿Qué Soluciona Este Proyecto?

Este proyecto automatiza el flujo completo de procesar y analizar audios mediante IA. Es útil para:

- Personas que necesitan transcribir reuniones o notas de voz.
- Usuarios que desean generar resúmenes claros y estructurados de contenido hablado.
- Procesar grandes volúmenes de audios de manera eficiente y organizada.

# backend/Dockerfile

# Etapa 1: Construcción
FROM python:3.10-slim AS builder

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar archivos de requisitos
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --upgrade pip \
    && pip install --user -r requirements.txt

# Etapa 2: Imagen final
FROM python:3.10-slim

# Instalar dependencias del sistema necesarias en runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar dependencias desde la etapa de construcción
COPY --from=builder /root/.local /root/.local

# Añadir el directorio de usuarios a PATH
ENV PATH=/root/.local/bin:$PATH

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto en el que correrá FastAPI
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

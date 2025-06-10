# backend/Dockerfile
FROM python:3.11-slim

# Set work dir
WORKDIR /app

# Copiar los archivos
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir flask flask-cors

# Exponer el puerto
EXPOSE 5000

# Comando para iniciar Flask
CMD ["python", "app.py"]

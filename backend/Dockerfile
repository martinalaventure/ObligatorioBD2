# backend/Dockerfile
FROM python:3.11-slim

# Set work dir
WORKDIR /usr/src/app

# Copiar los archivos
COPY requirements.txt ./

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# Exponer el puerto
EXPOSE 5000

# Comando para iniciar Flask
CMD ["python", "app.py"]

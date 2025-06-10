# frontend/Dockerfile
FROM node:20

# Set work dir
WORKDIR /app

# Copiar archivos
COPY . .

# Instalar dependencias y construir
RUN npm install
RUN npm run build

# Instalar un servidor para servir la app
RUN npm install -g serve

# Exponer el puerto
EXPOSE 3000

# Comando para correr la app
CMD ["serve", "-s", "build", "-l", "3000"]

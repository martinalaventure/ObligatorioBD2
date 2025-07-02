# frontend/Dockerfile
FROM node:20

# Set work dir
WORKDIR /usr/src/app

# Copiar archivos
COPY package.json package-lock.json ./

# Instalar dependencias y construir
RUN npm install

COPY . .

RUN npm run build

# Exponer el puerto
EXPOSE 3000

# Comando para correr la app
CMD ["npm", "run", "dev"]

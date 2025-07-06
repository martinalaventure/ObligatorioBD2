# ObligatorioBD2

En este repositorio está el desarrollo del obligatorio de Bases de Datos 2, semestre 1 de 2025

## Uso

### Primer forma de correr el programa
Ubicarse en la ruta del proyecto ```../ObligatorioBD2``` y desde la terminal correr el comando ```docker-compose up --build``` para poder levantar los contenedores en docker. D esta manera luego se puede acceder a la ruta proporcionada en la terminal o ```localhost:3000```.

### Segunda forma de correr el programa
Dejamos a disposición una segunda forma de correr el programa en caso de que la anterior no funcione correctamente.
Para ello se deben de disponer dos terminales una creada para la ruta ```../ObligatorioBD2/backend``` y otra para la ruta ```../ObligatorioBD2/frontend```.

En ```../ObligatorioBD2/backend```:
Correr el comando ```python app.py``` o ```py app.py```. Esto levantará el servidor de Flask.

En ```../ObligatorioBD2/frontend```:
Correr el comando ```npm install```, luego ```npm start```

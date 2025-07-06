from conexion import obtener_conexion
from datetime import datetime, timedelta
import random

conexion = obtener_conexion()
cursor = conexion.cursor()

#obtenemos todos los circuitos con su serie y desde-hasta
cursor.execute("SELECT Serie, Desde, Hasta FROM Circuito")
circuitos = cursor.fetchall()

nombres = ["Ana", "Luis", "Carla", "Diego", "Lucía", "Pedro", "Mario", "Agustina", "Camila", "Pablo"]
apellidos = ["Gómez", "Pérez", "Fernández", "Rodríguez", "Silva", "López", "Montero", "Gonzalez", "Arias"]

for i in range(1, 501):
    ci = f"{50000000 + i}"
    
    #se elije un circuito aleatorio y  generamos la cc del ciudadano
    serie, desde, hasta = random.choice(circuitos)
    numero_cc = random.randint(desde, hasta)
    cc = f"{serie}{numero_cc:04d}"

    nombre = random.choice(nombres)
    apellido = random.choice(apellidos)
    nacimiento = datetime(1960, 1, 1) + timedelta(days=random.randint(7000, 20000))
    nacimiento_str = nacimiento.strftime("%Y-%m-%d")

    cursor.execute("""
        INSERT INTO Ciudadano (CI, CC, Nombre, Apellido, F_Nacimiento)
        VALUES (%s, %s, %s, %s, %s)
    """, (ci, cc, nombre, apellido, nacimiento_str))

conexion.commit()
cursor.close()
conexion.close()
print("Ciudadanos insertados correctamente con CC coherente")



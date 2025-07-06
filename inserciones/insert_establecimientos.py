from conexion import obtener_conexion
import random

conexion = obtener_conexion()
cursor = conexion.cursor()

tipos = ["Escolar", "Técnico", "Universitario"]

for i in range(1, 101):
    nombre = f"Establecimiento {i}"
    direccion = f"Calle Establecimiento {i} #{random.randint(1, 999)}"
    tipo = random.choice(tipos)
    id_zona = random.randint(1, 100)  

    cursor.execute("""
        INSERT INTO Establecimiento (ID, Nombre, Direccion, Tipo, ID_Zona)
        VALUES (%s, %s, %s, %s, %s)
    """, (i, nombre, direccion, tipo, id_zona))

conexion.commit()
cursor.close()
conexion.close()
print("Establecimientos insertados correctamente")

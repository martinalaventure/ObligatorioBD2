from conexion import obtener_conexion
import random

conexion = obtener_conexion()
cursor = conexion.cursor()

tipos = ["Urbana", "Suburbana", "Rural"]

for i in range(1, 300):
    nombre = f"Zona {i}"
    tipo = random.choice(tipos)
    id_depto = random.randint(1, 19)  

    cursor.execute("""
        INSERT INTO Zona (ID, Nombre, Tipo, ID_Departamento)
        VALUES (%s, %s, %s, %s)
    """, (i, nombre, tipo, id_depto))

conexion.commit()
cursor.close()
conexion.close()
print("Zonas insertadas correctamente")

from conexion import obtener_conexion
import random

conexion = obtener_conexion()
cursor = conexion.cursor()

for partido_id in range(1, 9):
    ci_autoridad = str(40000000 + random.randint(1, 100))

    cursor.execute("""
        INSERT INTO Autoridad (ID_Partido, CI_Autoridad)
        VALUES (%s, %s)
    """, (partido_id, ci_autoridad))

conexion.commit()
cursor.close()
conexion.close()
print("Autoridades asignadas a partidos correctamente")
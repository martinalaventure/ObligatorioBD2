from conexion import obtener_conexion
import random

conexion = obtener_conexion()
cursor = conexion.cursor()

for i in range(1, 1000):
    id_depto = random.randint(1, 19)       # departamentos ya insertados
    id_partido = random.randint(1, 8)     # partidos ya insertados
    id_evento = random.randint(1, 3)      # eentos ya insertados

    cursor.execute("""
        INSERT INTO Lista (Numero, ID_Departamento, ID_Partido, ID_Evento_Electoral)
        VALUES (%s, %s, %s, %s)
    """, (i, id_depto, id_partido, id_evento))

conexion.commit()
cursor.close()
conexion.close()
print("Listas insertadas correctamente")

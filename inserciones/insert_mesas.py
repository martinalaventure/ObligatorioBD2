from conexion import obtener_conexion
import random

conexion = obtener_conexion()
cursor = conexion.cursor()

for i in range(2, 501):
    total = random.randint(0, 500)
    id_circuito = random.randint(1, 400)  # circuitos ya insertados

    cursor.execute("""
        INSERT INTO Mesa (ID, Total_Votos_Emitidos, ID_Circuito)
        VALUES (%s, %s, %s)
    """, (i, total, id_circuito))

conexion.commit()
cursor.close()
conexion.close()
print("Mesas insertadas correctamente")

from conexion import obtener_conexion
import random

conexion = obtener_conexion()
cursor = conexion.cursor()

for i in range(2, 401):
    accesible = random.choice([True, False])
    serie = f"Serie-{random.randint(1000, 9999)}"
    desde = random.randint(40000000, 40000100)
    hasta = desde + random.randint(10, 50)
    id_est = random.randint(1, 100)  # establecimientos que ya insertamos

    cursor.execute("""
        INSERT INTO Circuito (ID, Accesible, Serie, Desde, Hasta, ID_Establecimiento)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (i, accesible, serie, desde, hasta, id_est))

conexion.commit()
cursor.close()
conexion.close()
print("Circuitos insertados correctamente")

from conexion import obtener_conexion
import random

conexion = obtener_conexion()
cursor = conexion.cursor()

for i in range(1, 301):
    direccion = f"Calle Comisaria {i} #{random.randint(1, 999)}"
    id_depto = random.randint(1, 19)

    cursor.execute("""
        INSERT INTO Comisaria (ID, Direccion, ID_Departamento)
        VALUES (%s, %s, %s)
    """, (i, direccion, id_depto))

conexion.commit()
cursor.close()
conexion.close()
print("Comisarías insertadas correctamente")

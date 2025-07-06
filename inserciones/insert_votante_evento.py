from conexion import obtener_conexion
import random

conexion = obtener_conexion()
cursor = conexion.cursor()

for i in range(401, 501):
    ci = f"{50000000 + i}"
    evento_id = random.randint(1, 3)

    # verificamos si la ci existe
    cursor.execute("SELECT 1 FROM Votante WHERE CI = %s", (ci,))
    if cursor.fetchone() is None:
        print(f"Votante con CI={ci} no existe. Saltando.")
        continue

    # verificamos si el id del evento existe
    cursor.execute("SELECT 1 FROM Evento_Electoral WHERE ID = %s", (evento_id,))
    if cursor.fetchone() is None:
        print(f"Evento con ID={evento_id} no existe. Saltando.")
        continue

    try:
        cursor.execute("""
            INSERT INTO Votante_Participa_Evento (CI_Votante, ID_Evento_Electoral)
            VALUES (%s, %s)
        """, (ci, evento_id))
        print(f"Insertado: CI={ci}, Evento={evento_id}")
    except Exception as e:
        print(f"Error al insertar CI={ci}, Evento={evento_id}: {e}")

conexion.commit()
cursor.close()
conexion.close()
print("Inserciones para votante_particpa_en_evento realizadas correctamente")
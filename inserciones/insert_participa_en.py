from conexion import obtener_conexion
import random

conexion = obtener_conexion()
cursor = conexion.cursor()

for _ in range(300, 400):  # insertamos relaciones
    evento_id = random.randint(1, 3)      # los 3 eventos
    partido_id = random.randint(1, 8)     # los 8 partidos

    try:
        cursor.execute("""
            INSERT INTO Participa_En (ID_EventoElectoral, ID_Partido)
            VALUES (%s, %s)
        """, (evento_id, partido_id))
    except Exception as e:
        print(f"Error al insertar Evento={evento_id}, Partido={partido_id}: {e}")

conexion.commit()
cursor.close()
conexion.close()
print("Relaciones Participa_En insertadas correctamente")
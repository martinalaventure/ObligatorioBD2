from conexion import obtener_conexion
from datetime import datetime

conexion = obtener_conexion()
cursor = conexion.cursor()

eventos = [ #eleccines nacionales previamente ingresado
    (2, "Balotaje 2025", "2025-11-24"),
    (3, "Elecciones Internas", "2025-06-30")
]

for evento in eventos:
    cursor.execute("""
        INSERT INTO Evento_Electoral (ID, Tipo, Fecha)
        VALUES (%s, %s, %s)
    """, evento)

conexion.commit()
cursor.close()
conexion.close()

print("Eventos electorales insertados correctamente")

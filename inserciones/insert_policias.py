from conexion import obtener_conexion
import random

conexion = obtener_conexion()
cursor = conexion.cursor()

# obtenemos todos los ci disponibles en ciudadano
cursor.execute("SELECT CI FROM Ciudadano")
cis_validos = [row[0] for row in cursor.fetchall()]

# cbtenemos los ids de establecimiento y comisaria
cursor.execute("SELECT ID FROM Establecimiento")
establecimientos = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT ID FROM Comisaria")
comisarias = [row[0] for row in cursor.fetchall()]

insertados = 0

for ci in random.sample(cis_validos, min(50, len(cis_validos))):
    id_est = random.choice(establecimientos)
    id_com = random.choice(comisarias)

    try:
        cursor.execute("""
            INSERT INTO Policia (CI, ID_Establecimiento, ID_Comisaria)
            VALUES (%s, %s, %s)
        """, (ci, id_est, id_com))
        insertados += 1
    except Exception as e:
        print(f"Error al insertar CI={ci}: {e}")

conexion.commit()
cursor.close()
conexion.close()
print(f"Policías insertados: {insertados}")
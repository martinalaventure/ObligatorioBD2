from conexion import obtener_conexion
import random
import string

conexion = obtener_conexion()
cursor = conexion.cursor()

# obtenemos los ci de ciudadanos
cursor.execute("SELECT CI FROM Ciudadano")
ciudadanos = cursor.fetchall()

for (ci,) in ciudadanos:
    # verificamos si ya existe en la tabla votante
    cursor.execute("SELECT 1 FROM Votante WHERE CI = %s", (ci,))
    existe = cursor.fetchone()

    if existe:
        continue  #  si ya esta pasamos al siguiente

    habilitado = random.choice([1, 0])
    voto = random.choice([1, 0]) if habilitado == 1 else 0
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=20))

    cursor.execute("""
        INSERT INTO Votante (CI, Habilitado, Voto, Token_Inicial)
        VALUES (%s, %s, %s, %s)
    """, (ci, habilitado, voto, token))

conexion.commit()
cursor.close()
conexion.close()
print("Votantes insertados sin duplicados correctamente")
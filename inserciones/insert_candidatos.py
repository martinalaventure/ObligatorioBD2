from conexion import obtener_conexion
import random

conexion = obtener_conexion()
cursor = conexion.cursor()

for i in range(1, 41):  #vamos mofificando de acuerso a las inserciones
    ci = f"{40000000 + i}"
    organo = random.choice(["Senado", "Cámara", "Junta Electoral","Gobierno"])
    cargo = random.choice(["Senador", "Diputado", "Edil", "Presidente", "Vicepresidente", "Suplente"])
    lugar = random.randint(1, 10)
    id_partido = random.randint(1, 8)

    cursor.execute("""
        INSERT INTO Candidato (CI, Organo, Cargo, Lugar_En_Lista, ID_Partido)
        VALUES (%s, %s, %s, %s, %s)
    """, (ci, organo, cargo, lugar, id_partido))

conexion.commit()
cursor.close()
conexion.close()
print("Candidatos insertados correctamente")
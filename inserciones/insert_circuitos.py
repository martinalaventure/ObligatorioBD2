from conexion import obtener_conexion
import random
import string

conexion = obtener_conexion()
cursor = conexion.cursor()

letras_usadas = set()

def generar_serie(letras_existentes):
    while True:
        letras = ''.join(random.choices(string.ascii_uppercase, k=3))
        if letras not in letras_existentes:
            letras_existentes.add(letras)
            return letras

for i in range(1, 301):
    accesible = random.choice([True, False])
    serie = generar_serie(letras_usadas)
    desde = random.randint(1000, 5000)
    hasta = desde + random.randint(50, 200)
    id_est = random.randint(1, 100)

    cursor.execute("""
        INSERT INTO Circuito (ID, Accesible, Serie, Desde, Hasta, ID_Establecimiento)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (i, accesible, serie, desde, hasta, id_est))

conexion.commit()
cursor.close()
conexion.close()
print("Circuitos creados correctamente")
from conexion import obtener_conexion
import random

conexion = obtener_conexion()
cursor = conexion.cursor()

#obtenemos la cantidad de votos habilitados desde la tabla votante
cursor.execute("SELECT COUNT(*) FROM Votante WHERE Habilitado = TRUE")
votos_habilitados = cursor.fetchone()[0]

print(f"Votos habilitados totales: {votos_habilitados}")

#cantidad de mesas y circuitos disponibles
MESAS = 300
CIRCUITOS = 300 

# distribuimos los votos aleatoriamente entre mesas
votos_por_mesa = [0] * MESAS
for _ in range(votos_habilitados):
    idx = random.randint(0, MESAS - 1)
    votos_por_mesa[idx] += 1

for i in range(1, MESAS + 1): #insertamos las mesas con los votos ya asignados
    total = votos_por_mesa[i - 1]
    id_circuito = random.randint(1, CIRCUITOS)

    cursor.execute("""
        INSERT INTO Mesa (ID, Total_Votos_Emitidos, ID_Circuito)
        VALUES (%s, %s, %s)
    """, (i, total, id_circuito))

conexion.commit()
cursor.close()
conexion.close()
print("Mesas insertadas correctamente con votos realistas")

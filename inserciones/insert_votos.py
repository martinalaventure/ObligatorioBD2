from conexion import obtener_conexion
import random
from datetime import datetime, timedelta

conexion = obtener_conexion()
cursor = conexion.cursor()

# obtenemos lso circuitos
cursor.execute("SELECT ID FROM Circuito")
circuitos = [row[0] for row in cursor.fetchall()]

# obtenemos las listas válidas
cursor.execute("SELECT Numero FROM Lista")
listas = [row[0] for row in cursor.fetchall()]

if not circuitos or not listas:
    print("Faltan circuitos o listas.")
    exit()

for i in range(101, 451): #podemos ir vairando la cantidad de votos a insertar
    fecha_hora = datetime.now() - timedelta(days=random.randint(0, 10))
    circuito_id = random.choice(circuitos)

    en_blanco = 1 if random.random() < 0.2 else 0
    anulado = 0
    observado = 0
    numero_lista = None

    if en_blanco == 0:
        anulado = 1 if random.random() < 0.1 else 0
        if anulado == 0:
            observado = 1 if random.random() < 0.15 else 0
            numero_lista = random.choice(listas)  # solo si es valido

    try:
        cursor.execute("""
            INSERT INTO Voto (En_Blanco, Anulado, Observado, Fecha_Hora, Numero_Lista, ID_Circuito)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            en_blanco,
            anulado,
            observado,
            fecha_hora.strftime('%Y-%m-%d %H:%M:%S'),
            numero_lista,
            circuito_id
        ))
    except Exception as e:
        print(f"Error al insertar voto #{i}: {e}")

conexion.commit()
cursor.close()
conexion.close()
print("Votos insertados correctamente")
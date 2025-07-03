from conexion import obtener_conexion
import random
import string
import hashlib

conexion = obtener_conexion()
cursor = conexion.cursor()

# obtenemos la ci de ciudadanos (que no estén ya como empleados públicos)
cursor.execute("""
    SELECT CI FROM Ciudadano 
    WHERE CI NOT IN (SELECT CI FROM Empleado_Publico)
    LIMIT 50
""")
ciudadanos = cursor.fetchall()

# obtenemos las mesas para asignar
cursor.execute("SELECT ID FROM Mesa")
mesas = [row[0] for row in cursor.fetchall()]

organismos = ["Corte Electoral", "Ministerio del Interior", "Intendencia", "Junta Electoral", "ANEP", "Poder Judicial"]
roles = ["Presidente", "Vocal", "Escribano", "Auxiliar"]

for i, (ci,) in enumerate(ciudadanos):
    organismo = random.choice(organismos)
    rol = random.choice(roles)
    id_mesa = random.choice(mesas)
    usuario = f"user_{ci}"
    password_plano = f"clave{ci}"
    password_hash = hashlib.sha256(password_plano.encode()).hexdigest()

    cursor.execute("""
        INSERT INTO Empleado_Publico 
        (CI, Organismo_De_Trabajo, Rol_En_Mesa, ID_Mesa, Usuario, Password_Hash)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (ci, organismo, rol, id_mesa, usuario, password_hash))

conexion.commit()
cursor.close()
conexion.close()
print("Empleados públicos insertados correctamente.")

#PARTIDOS INGRESADOS MANUALMENTE, si necesitamos m'as los pasamos al script para ingresar
# from conexion import obtener_conexion

# conexion = obtener_conexion()
# cursor = conexion.cursor()

# partidos = [
#     (1, "Partido Nacional"),
#     (2, "Frente Amplio"),
#     (3, "Partido Colorado"),
#     (4, "Cabildo Abierto")
# ]

# for partido in partidos:
#     cursor.execute("""
#         INSERT INTO Partido_Politico (ID, Nombre)
#         VALUES (%s, %s)
#     """, partido)

# conexion.commit()
# cursor.close()
# conexion.close()

# print("Partidos políticos insertados correctamente")

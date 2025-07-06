import mysql.connector

def obtener_conexion():
    return mysql.connector.connect(
        host="mysql.reto-ucu.net",
        port=50006,
        user="am_g3_admin",
        password="6rup0_3_8ASES",
        database="AM_Grupo3"
    )

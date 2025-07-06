from datetime import datetime, time
from zoneinfo import ZoneInfo
from zoneinfo import ZoneInfo
from flask import Flask, request, jsonify
import secrets
from mysql.connector import Error
from flask_cors import CORS
import mysql.connector
import os
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash

load_dotenv()

app = Flask(__name__)
CORS(app)

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT", 3306))
        )
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

@app.route('/')
def home():
    return "Hola desde Flask con MySQL conectado!"

@app.route('/dbcheck')
def dbcheck():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=os.getenv("DB_PORT", 3306)
        )
        return "Conexión a MySQL exitosa!"
    except Exception as e:
        return f"Error de conexión: {str(e)}"
    
@app.route('/login/votante', methods=['POST'])
def login_votante():
    data = request.get_json()

    # Validación básica
    if not data or not data.get('serie') or not data.get('cc') or not data.get('circuito_id'):
        return jsonify({'error': 'Serie, Credencial y Circuito son requeridos'}), 400

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Error de conexión con la base de datos'}), 500

        cursor = conn.cursor(dictionary=True)

        # Buscar al votante
        cursor.execute("""
            SELECT c.CI, c.CC, c.Nombre, c.Apellido, v.Habilitado, v.Voto
            FROM Ciudadano c
            LEFT JOIN Votante v ON c.CI = v.CI
            JOIN Circuito ci ON ci.Serie = %s AND ci.ID = %s
            WHERE c.CC = %s
        """, (data['serie'], data['circuito_id'], data['cc']))

        votante = cursor.fetchone()

        if not votante:
            return jsonify({'error': 'Datos incorrectos'}), 401

        if not votante.get('Habilitado', False):
            return jsonify({'error': 'No estás habilitado para votar'}), 403

        if votante.get('Voto', False):
            return jsonify({'error': 'Ya has ejercido tu derecho al voto'}), 403

        token = secrets.token_urlsafe(32)

        cursor.execute("""
            INSERT INTO Votante (CI, Habilitado, Voto, Token_Inicial)
            VALUES (%s, TRUE, FALSE, %s)
            ON DUPLICATE KEY UPDATE Token_Inicial = %s
        """, (votante['CI'], token, token))

        conn.commit()

        return jsonify({
            'message': 'Autenticación exitosa',
            'token': token,
            'user_data': {
                'ci': votante['CI'],
                'nombre': f"{votante['Nombre']} {votante['Apellido']}"
            }
        }), 200

    except Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Error en el servidor'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

@app.route('/login/admin', methods=['POST'])
def login_admin():
    data = request.get_json()

    if not data or not data.get('usuario') or not data.get('contrasena'):
        return jsonify({'error': 'Usuario y contraseña son requeridos'}), 400

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Error de conexión con la base de datos'}), 500

        cursor = conn.cursor(dictionary=True)

        # Buscar admin por usuario
        cursor.execute("""
            SELECT CI, Usuario, Password_Hash
            FROM Admin
            WHERE Usuario = %s
        """, (data['usuario'],))

        admin = cursor.fetchone()

        # Verificar credenciales
        if not admin or not check_password_hash(admin['Password_Hash'], data['contrasena']):
            return jsonify({'error': 'Usuario o contraseña incorrectos'}), 401

        # Generar token 
        token = secrets.token_urlsafe(32)

        return jsonify({
            'message': 'Autenticación exitosa',
            'token': token,
            'user_data': {
                'ci': admin['CI'],            }
        }), 200

    except Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Error en el servidor'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

@app.route('/login/presidente', methods=['POST'])
def login_presidente():
    data = request.get_json()

    if not data or not data.get('usuario') or not data.get('contrasena'):
        return jsonify({'error': 'Usuario y contraseña son requeridos'}), 400

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Error de conexión con la base de datos'}), 500

        cursor = conn.cursor(dictionary=True)

        # Buscar admin por usuario
        cursor.execute("""
            SELECT CI, Usuario, Password_Hash
            FROM Empleado_Publico
            WHERE Usuario = %s
        """, (data['usuario'],))

        admin = cursor.fetchone()

        # Verificar credenciales
        if not admin or not check_password_hash(admin['Password_Hash'], data['contrasena']):
            return jsonify({'error': 'Usuario o contraseña incorrectos'}), 401

        # Generar token
        token = secrets.token_urlsafe(32)

        return jsonify({
            'message': 'Autenticación exitosa',
            'token': token,
            'ci': admin['CI']
        }), 200

    except Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Error en el servidor'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def obtener_resumen_votos(circuito_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute("""
            SELECT
                l.Numero                              AS numero_lista,
                COALESCE(p.Nombre, 'Sin partido')     AS partido,
                COUNT(v.ID_Voto)                      AS cantidad,
                v.ID_Circuito                         AS circuito_id 
            FROM Voto v
            LEFT JOIN Lista            l ON v.Numero_Lista = l.Numero
            LEFT JOIN Partido_Politico p ON l.ID_Partido   = p.ID
            WHERE v.ID_Circuito = %s
            GROUP BY l.Numero, p.Nombre
        """, (circuito_id,))
        votos = cur.fetchall()

        total_validos = sum(
            v['cantidad'] for v in votos
            if v['partido'].lower() not in ['anulados', 'en blanco']
        )

        resultado = []
        for v in votos:
            partido_lower = (v['partido'] or '').lower()
            es_valido = partido_lower not in ['anulados', 'en blanco']
            porcentaje = round(v['cantidad'] * 100 / total_validos, 2) if es_valido and total_validos > 0 else 0.0
            resultado.append({
                'numero_lista'     : v['numero_lista'],
                'partido'          : v['partido'],
                'cantidad'         : v['cantidad'],
                'circuito_id'      : v['circuito_id'],
                'porcentaje_validos': porcentaje
            })

        return {'total_validos': total_validos, 'votos': resultado}
    finally:
        cur.close()
        conn.close()

@app.route('/presidente', methods=['POST'])
def datos_presidente():
    data = request.get_json()
    ci = data.get('ci')

    if not ci:
        return jsonify({'error': 'CI requerido'}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Obtener circuito del presidente
    cursor.execute("""
        SELECT c.ID AS circuito_id
        FROM Empleado_Publico ep
        JOIN Mesa m ON ep.ID_Mesa = m.ID
        JOIN Circuito c ON m.ID_Circuito = c.ID
        WHERE ep.CI = %s
        """, (ci,))
    mesa_data = cursor.fetchone()

    if not mesa_data:
        return jsonify({'error': 'Presidente no asociado a ninguna mesa'}), 404

    circuito_id = mesa_data['circuito_id']

    resumen = obtener_resumen_votos(circuito_id)
    return jsonify(resumen), 200

@app.route('/presidente/iniciar', methods=['POST'])
def iniciar_votacion():
    data = request.get_json()
    circuito_id = data.get('circuito_id')

    ahora = datetime.now(ZoneInfo("America/Montevideo")).time()
    if not (time(8, 0) <= ahora <= time(19, 30)):
        return jsonify({'error': 'Fuera del horario permitido (08:00‑19:30)'}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE Circuito SET abierto = TRUE WHERE ID = %s", (circuito_id,))
        conn.commit()
        return jsonify({'message': 'Votación iniciada'}), 200
    except Exception as e:
        conn.rollback()
        print(e)
        return jsonify({'error': 'Error en servidor'}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/presidente/finalizar', methods=['POST'])
def finalizar_votacion():
    circuito_id = request.get_json().get('circuito_id')
    data = request.get_json()
    circuito_id = data.get('circuito_id')

    ahora = datetime.now(ZoneInfo("America/Montevideo")).time()
    if ahora <= time(19, 30):
        return jsonify({'error': 'Solo se puede finalizar después de las 19:30'}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT abierto FROM Circuito WHERE ID = %s", (circuito_id,))
    estado = cursor.fetchone()
    if not estado or not estado['abierto']:
        return jsonify({'error': 'La votación no estaba activa'}), 400

    cursor.execute("UPDATE Circuito SET abierto = FALSE WHERE ID = %s", (circuito_id,))
    conn.commit()
    resumen = obtener_resumen_votos(circuito_id)  
    return jsonify({'message': 'Votación finalizada', **resumen}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
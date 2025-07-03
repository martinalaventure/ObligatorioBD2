from flask import Flask, request, jsonify
import secrets
from mysql.connector import Error
from flask_cors import CORS
import mysql.connector
import os
from dotenv import load_dotenv
from functools import wraps
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

def token_required(f):
    '''Esta función provee seguridad para la página, chequea el token del votante para autorizarlo a que pueda votar'''
    @wraps(f)
    def decorated(*args, **kwargs):
        token_header = request.headers.get('Authorization')
        if not token_header or not token_header.startswith('Bearer '):
            return jsonify({'error': 'Token no proporcionado'}), 401
        
        token = token_header.split(' ')[1]

        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            if not conn:
                return jsonify({'error': 'Error de conexión'}), 500
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT * FROM Votante WHERE Token_Inicial = %s AND Habilitado = TRUE AND Voto = FALSE
            """, (token,))
            votante = cursor.fetchone()

            if not votante:
                return jsonify({'error': 'Token inválido o expirado'}), 403
            
            
            return f( *args, **kwargs)
        
        except Error as e:
            print(f"Token check DB error: {e}")
            return jsonify({'error': 'Error del servidor'}), 500
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
    return decorated 
    
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

@app.route('/presidente', methods=['POST'])
def datos_presidente():
    data = request.get_json()
    ci = data.get('ci')

    if not ci:
        return jsonify({'error': 'CI requerido'}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
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

        # Obtener votos por lista/partido, incluyendo partidos "En Blanco" y "Anulados"
        cursor.execute("""
            SELECT
                l.Numero                              AS numero_lista,
                COALESCE(p.Nombre, 'Sin partido')     AS partido,
                COUNT(v.ID_Voto)                      AS cantidad
            FROM Voto v
            LEFT JOIN Lista l           ON v.Numero_Lista = l.Numero
            LEFT JOIN Partido_Politico p ON l.ID_Partido   = p.ID
            WHERE v.ID_Circuito = %s
            GROUP BY l.Numero, p.Nombre
            ORDER BY cantidad DESC
        """, (circuito_id,))
        votos = cursor.fetchall()

        # Calcular total de votos válidos (excluye partidos anulados o en blanco)
        total_validos = sum(
            v['cantidad'] for v in votos
            if v['partido'].lower() not in ['anulados', 'enblanco']
        )

        # Armar respuesta con porcentaje de votos válidos
        resultado = []
        for v in votos:
            partido_lower = v['partido'].lower()
            es_valido = partido_lower not in ['anulados', 'enblanco']

            porcentaje = round(v['cantidad'] * 100 / total_validos, 2) if es_valido and total_validos > 0 else 0.0

            resultado.append({
                'numero_lista'     : v['numero_lista'],
                'partido'          : v['partido'],
                'cantidad'         : v['cantidad'],
                'porcentaje_validos': porcentaje
            })

        return jsonify({
            'total_validos': total_validos,
            'votos'        : resultado
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Error interno del servidor'}), 500
    finally:
        cursor.close()
        conn.close()




@app.route('/listas', methods=['GET'])
@token_required
def obtener_listas_para_votar():
    '''Esta ruta es donde el votante verá desplegada la vista con las diferentes listas para votar.'''
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Error de conexión con la base de datos'}), 500
        cursor = conn.cursor(dictionary=True)
        #Obtener todas las listas
        cursor.execute("""
            SELECT Lista.Numero, Partido_Politico.Nombre AS Nombre_Partido FROM Lista JOIN Partido_Politico ON Lista.ID_Partido = Partido_Politico.ID
        """)
        listas = cursor.fetchall()
        
        return jsonify({'listas': listas}), 200

    except Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Error en el servidor'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

@app.route('/listas/<id>', methods = ['GET'])
@token_required
def obtener_info_de_una_lista(id):
    '''Esta ruta es para obtener la vista de una lista seleccionada'''
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Error de conexión con la base de datos'}), 500
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT Lista.Numero, Departamento.Nombre AS Nombre_Departamento, Partido_Politico.Nombre AS Nombre_Partido, Partido_Politico.Dir_Sede, Evento_Electoral.Tipo
            FROM Lista 
                       JOIN Departamento ON Lista.ID_Departamento = Departamento.ID
                       JOIN Partido_Politico ON Lista.ID_Partido = Partido_Politico.ID
                       JOIN Evento_Electoral ON Lista.ID_Evento_Electoral = Evento_Electoral.ID
            WHERE Lista.Numero = %s
        """,(id,))

        lista = cursor.fetchone()

        if not lista:
            return jsonify({'error': 'Lista no encontrada'}), 404

        return jsonify({'lista': lista}), 200

    except Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Error en el servidor'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

# @app.route('/votar', methods=['POST'])
# @token_required
# def registrar_voto():
#     '''Esta ruta es para poder registrar un voto a una lista elegida por el votante'''
#     data = request.get_json()
#     id_lista = data.get('numero_Lista')
#     en_blanco = data.get('en_blanco', False)
#     anulado = data.get('anulado', False)
#     id_circuito = data.get('id_circuito')

#     if not en_blanco and not anulado and not id_lista and not id_circuito:
#         return jsonify({'error': 'Debe votar por una lista o votar en blanco o anulado y votar en un circuito habilitado'}), 400

#     auth_header = request.headers.get('Authorization')
#     token = auth_header.split(' ')[1]

#     conn = None
#     cursor = None
#     try:
#         conn = get_db_connection()
#         if not conn:
#             return jsonify({'error': 'Error de conexión con la base de datos'}), 500
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute('''

#         ''')




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
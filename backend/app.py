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
            
            # Pasar votante como argumento
            return f(votante, *args, **kwargs)
        
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
    if not data or not data.get('cc') or not data.get('circuito_id'):
        return jsonify({'error': 'Credencial y Circuito son requeridos'}), 400

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Error de conexión con la base de datos'}), 500

        cursor = conn.cursor(dictionary=True)

        # Buscar al votante
        #JOIN Circuito ci ON ci.Serie = %s AND ci.ID = %s eliminada para que no tenga que restringir la votación 
        cursor.execute("""
            SELECT c.CI, c.CC, c.Nombre, c.Apellido, v.Habilitado, v.Voto
            FROM Ciudadano c
            LEFT JOIN Votante v ON c.CI = v.CI
            WHERE c.CC = %s
        """, (data['cc'],))

        votante = cursor.fetchone()

        if not votante:
            return jsonify({'error': 'Datos incorrectos'}), 401

        #Acá estaríamos validando que la serie coincida con la serie del votante
        serie_votante = votante['CC'][:3]

        cursor.execute("SELECT Serie FROM Circuito WHERE ID = %s", (data['circuito_id'],))
        circuito = cursor.fetchone()

        if not circuito:
            return jsonify({'error': 'Circuito no encontrado'}), 404

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
            'serie': serie_votante,
            'circuito': data['circuito_id'],
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
def obtener_listas_para_votar(_):
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
            SELECT Lista.Numero, Partido_Politico.Nombre AS Nombre_Partido 
                       FROM Lista 
                       JOIN Partido_Politico ON Lista.ID_Partido = Partido_Politico.ID
                       WHERE Lista.Numero NOT IN (1, 2)
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
def obtener_info_de_una_lista(_, id):
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
                       LEFT JOIN Departamento ON Lista.ID_Departamento = Departamento.ID
                        JOIN Partido_Politico ON Lista.ID_Partido = Partido_Politico.ID
                       LEFT JOIN Evento_Electoral ON Lista.ID_Evento_Electoral = Evento_Electoral.ID
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

@app.route('/votar', methods=['POST'])
@token_required
def registrar_voto(votante):
    '''Esta ruta es para poder registrar un voto a una lista elegida por el votante'''
    data = request.get_json()
    id_lista = data.get('numero_Lista')
    en_blanco = data.get('en_blanco', False)
    anulado = data.get('anulado', False)
    id_circuito = data.get('id_circuito')
    serie_votante = data.get('serie')

    if not (en_blanco or anulado or id_lista):
        return jsonify({'error': 'Debe votar por una lista, o votar en blanco o anulado'}), 400
    if not id_circuito or not serie_votante:
        return jsonify({'error': 'Faltan datos de circuito o serie del votante'}), 400
   
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(' ')[1]

    conn = None
    cursor = None

    #Buscar la serie del circuito
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Error de conexión con la base de datos'}), 500
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
             SELECT Serie FROM Circuito WHERE ID = %s
        ''', (id_circuito,))
        circuito = cursor.fetchone()

        if not circuito:
            return jsonify({'error': 'Circuito no encontrado'}), 404
        
        serie_circuito = circuito['Serie']
        print("esta es serie_circuito" + serie_circuito)

        observado = (serie_votante != serie_circuito)

        #Insertar el voto en la tabla
        cursor.execute('''
            INSERT INTO Voto (En_Blanco, Anulado, Observado, Fecha_Hora, Numero_Lista, ID_Circuito)
                       VALUES (%s, %s, %s, NOW(), %s, %s)
        ''',(
            en_blanco,
            anulado,
            observado,
            id_lista,
            id_circuito
        ))
        conn.commit()

        cursor.execute('''
            UPDATE Votante 
            SET Voto = TRUE, Token_Inicial = NULL
            WHERE CI = %s
        ''', (votante['CI'],))
        conn.commit()

    except Exception as e:
        print('Error al registrar voto:', e)
        return jsonify({'error': 'Error al registrar voto'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return jsonify({
        'mensaje': 'Voto registrado correctamente',
        'observado': observado
    }), 200




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
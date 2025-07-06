from flask import Flask, request, jsonify
import secrets
from mysql.connector import Error
from flask_cors import CORS
import mysql.connector
import os
from dotenv import load_dotenv
import csv
from io import StringIO
from flask import Response

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
#---------------------homeAdmin---------------------
@app.route('/escrutinio/nacional', methods=['GET'])
def escrutinio_nacional():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                e.ID AS Evento_ID,
                e.Tipo AS Evento_Tipo,
                l.Numero AS Numero_Lista, 
                p.Nombre AS Partido,
                COUNT(v.ID_Voto) AS Total_Votos
            FROM Voto v
            JOIN Lista l ON v.Numero_Lista = l.Numero
            JOIN Partido_Politico p ON l.ID_Partido = p.ID
            JOIN Evento_Electoral e ON l.ID_Evento_Electoral = e.ID
            GROUP BY e.ID, e.Tipo, l.Numero, p.Nombre
            ORDER BY e.ID, Total_Votos DESC
        """)

        resultados = cursor.fetchall()
        return jsonify(resultados), 200

    except Error as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Error al obtener el escrutinio nacional'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


@app.route('/auditoria/reporte', methods=['GET'])
def reporte_auditoria():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                c.ID AS Circuito_ID,
                l.Numero AS Numero_Lista,
                p.Nombre AS Partido,
                COUNT(v.ID_Voto) AS Total_Votos
            FROM Voto v
            JOIN Circuito c ON v.ID_Circuito = c.ID
            JOIN Lista l ON v.Numero_Lista = l.Numero
            JOIN Partido_Politico p ON l.ID_Partido = p.ID
            GROUP BY c.ID, l.Numero, p.Nombre
            ORDER BY c.ID, Total_Votos DESC
        """)

        resultados = cursor.fetchall()

        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['Circuito_ID', 'Numero_Lista', 'Partido', 'Total_Votos'])
        for row in resultados:
            writer.writerow(row)

        output.seek(0)
        return Response(
            output.getvalue(), 
            mimetype='text/csv',
            headers={"Content-Disposition": "attachment;filename=reporte_auditoria_elecciones_nacionales.csv"}
        )

    except Error as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Error al generar el reporte'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

@app.route('/resultados/oficiales', methods=['GET'])
def resultados_oficiales():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # el ganador nacional
        cursor.execute("""
            SELECT p.Nombre AS Partido, COUNT(v.ID_Voto) AS Total_Votos
            FROM Voto v
            JOIN Lista l ON v.Numero_Lista = l.Numero
            JOIN Partido_Politico p ON l.ID_Partido = p.ID
            GROUP BY p.Nombre
            ORDER BY Total_Votos DESC
            LIMIT 1
        """)
        ganador_nacional = cursor.fetchone()

        #resultados por departamento
        cursor.execute("""
            SELECT d.Nombre AS Departamento, p.Nombre AS Partido, COUNT(v.ID_Voto) AS Total_Votos
            FROM Voto v
            JOIN Lista l ON v.Numero_Lista = l.Numero
            JOIN Partido_Politico p ON l.ID_Partido = p.ID
            JOIN Departamento d ON l.ID_Departamento = d.ID
            GROUP BY d.Nombre, p.Nombre
            ORDER BY d.Nombre, Total_Votos DESC
        """)
        rows = cursor.fetchall()

        resultados_por_departamento = {}
        for row in rows:
            depto = row['Departamento']
            if depto not in resultados_por_departamento:
                resultados_por_departamento[depto] = []
            resultados_por_departamento[depto].append({
                'Partido': row['Partido'],
                'Total_Votos': row['Total_Votos']
            })

        return jsonify({
            'ganador_nacional': ganador_nacional,
            'por_departamento': resultados_por_departamento
        })

    except Error as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Error al obtener resultados oficiales'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
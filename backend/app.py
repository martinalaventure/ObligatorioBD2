from flask import Flask
from flask_cors import CORS
import mysql.connector
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
CORS(app)

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


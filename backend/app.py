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
            host=os.getenv("DATABASE_HOST"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            database=os.getenv("DATABASE_NAME"),
            port=os.getenv("DATABASE_PORT", 3306)
        )
        return "Conexión a MySQL exitosa!"
    except Exception as e:
        return f"Error de conexión: {str(e)}"


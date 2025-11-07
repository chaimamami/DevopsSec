import os
import subprocess
from flask import Flask, request

app = Flask(__name__)

# Exemple de code vulnérable : commande Shell dangereuse
@app.route('/execute', methods=['POST'])
def execute_command():
    # Mauvaise pratique : utilisation de subprocess sans validation de l'entrée
    command = request.form['command']
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout

# Exemple de vulnérabilité : connexion sans chiffrement
def connect_to_db():
    connection = psycopg2.connect("dbname=test user=postgres")
    return connection

# Code vulnérable à l'injection SQL
def get_user_details(user_id):
    cursor = connection.cursor()
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    return cursor.fetchall()

# Code vulnérable à l'injection de dépendances
def unsafe_import():
    package = request.args.get('package')
    exec(f"import {package}")
    return f"Package {package} imported."

# Exemple d'utilisation d'une bibliothèque non sécurisée
import subprocess  # Mauvais usage de subprocess

@app.route('/')
def index():
    return "Hello, world!"

if __name__ == "__main__":
    app.run(debug=True)

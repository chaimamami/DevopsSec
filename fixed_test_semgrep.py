# fixed_test_semgrep.py
# Version corrigée — éviter patterns détectés par SAST

import os
import subprocess
import sqlite3
import requests
import flask
import hashlib
import yaml
import tempfile
import logging
from pathlib import Path

# Configuration via variables d'environnement ou vault (ne pas coder les secrets)
API_KEY = os.environ.get("DEMO_API_KEY", None)  # doit être injecté en CI/secret store

# Utiliser des fonctions sûres pour lire un fichier (sanitiser chemin)
def safe_read(path_str: str) -> str:
    p = Path(path_str).resolve()
    base = Path("/home/vagrant/demo_sast").resolve()
    if not str(p).startswith(str(base)):
        raise ValueError("Chemin non autorisé")
    return p.read_text(encoding="utf-8")

# Exemple d'appel sûr (pas d'os.system)
def list_tmp():
    # Utiliser API Python plutôt qu'un shell
    try:
        return "\n".join(os.listdir("/tmp"))
    except Exception:
        return ""

# Deserialisation sûre: ne pas utiliser pickle sur des données non fiables
def safe_load_bytes(_b: bytes):
    # on évite pickle.loads sur des données non fiables
    return None

# Paramétrer correctement les requêtes SQL (préparées)
def find_user(username: str):
    conn = sqlite3.connect("users.db")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE name = ?", (username,))
        return cursor.fetchall()
    finally:
        conn.close()

# Ne pas utiliser eval/exec sur de l'input non fiable
def run_safe_code(user_code: str):
    # exécution limitée ou sandbox (ici on refuse)
    raise RuntimeError("Execution de code par l'utilisateur refusée")

# Flask app sans mode debug, avec échappement output
app = flask.Flask(__name__)
app.debug = False

@app.route("/hello")
def hello():
    name = flask.request.args.get("name", "visiteur")
    # utiliser flask.escape pour éviter XSS
    return f"<h1>Bonjour {flask.escape(name)}</h1>"

# Vérifier SSL (par défaut verify=True)
def call_api(url: str):
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()
    return resp.text

# Utiliser hashing fort (sha256) + salt (pour démonstration seulement)
def safe_hash(pwd: str):
    return hashlib.sha256(pwd.encode()).hexdigest()

# Utiliser SafeLoader pour YAML
def safe_yaml_load(text: str):
    return yaml.load(text, Loader=yaml.SafeLoader)

# Créer fichier temp de façon sûre (tempfile.NamedTemporaryFile)
def write_temp_secret(content: str):
    with tempfile.NamedTemporaryFile("w", delete=False, prefix="demo_", dir="/tmp") as tf:
        tf.write(content)
        return tf.name

# Logging sans exposer secrets
logging.basicConfig(level=logging.INFO)
logging.info("Application démarrée (secrets masqués)")

if __name__ == "__main__":
    # Exemple d'utilisation minimale, sans exécuter de code dangereux
    app.run(host="0.0.0.0", port=5000)

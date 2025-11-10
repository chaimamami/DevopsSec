# test_semgrep.py
# Fichier de test volontairement vulnérable pour Semgrep + Bandit
# Place-le dans ton repo (ex: demo_sast/test_semgrep.py) et lance semgrep/bandit.

import os
import subprocess
import pickle
import sqlite3
import requests
import flask
import hashlib
import yaml
import tempfile

# ---------------------------
# 1) Secrets codés en dur (hardcoded secrets)
# ---------------------------
API_KEY = "AKIAAAAAAAAAAAAAAAAA"        # ❌ hardcoded secret (Semgrep / Gitleaks / Bandit B105)
DB_PASSWORD = "P@ssw0rd123"             # ❌ hardcoded password

# ---------------------------
# 2) Command injection / shell=True
# ---------------------------
user_file = input("Entrez un chemin de fichier: ")
os.system("cat " + user_file)            # ❌ concaténation → command injection (Bandit B602 / Semgrep)

subprocess.call("ls -la /tmp", shell=True)  # ❌ shell=True (Bandit B602)

# ---------------------------
# 3) Insecure deserialization
# ---------------------------
malformed = b"cos\nsystem\n(S'ls'\ntR."
# ❌ pickle.loads peut exécuter du code arbitraire (Bandit B301)
try:
    pickle.loads(malformed)
except Exception:
    pass

# ---------------------------
# 4) SQL injection
# ---------------------------
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
username = input("Username: ")
# ❌ interpolation directe → SQL injection (Semgrep)
query = f"SELECT * FROM users WHERE name = '{username}'"
cursor.execute(query)

# ---------------------------
# 5) Eval / exec dangereux
# ---------------------------
user_code = input("Entrez du code python: ")
# ❌ eval/exec = exécution arbitraire (Bandit B307 / Semgrep)
try:
    eval(user_code)
except Exception:
    pass

# ---------------------------
# 6) Flask debug / XSS / affichage utilisateur non-échappé
# ---------------------------
app = flask.Flask(__name__)
app.debug = True                          # ❌ expose stack traces / secrets

@app.route("/hello")
def hello():
    name = flask.request.args.get("name", "visiteur")
    # ❌ Renvoi direct d'entrée utilisateur → possible XSS (Semgrep)
    return f"<h1>Bonjour {name}</h1>"

# ---------------------------
# 7) Insecure HTTP (verify=False)
# ---------------------------
requests.get("https://example.com/api", verify=False)   # ❌ ignore la vérification SSL (Semgrep)

# ---------------------------
# 8) Weak hashing (MD5)
# ---------------------------
pwd = "mon_mot_de_passe"
md5hash = hashlib.md5(pwd.encode()).hexdigest()         # ❌ MD5 faible (Bandit B303)
print("MD5:", md5hash)

# ---------------------------
# 9) Unsafe YAML load
# ---------------------------
yaml_text = "!!python/object/apply:os.system ['echo vuln']"
# ❌ yaml.load sans SafeLoader (Semgrep / Bandit)
try:
    yaml.load(yaml_text, Loader=yaml.FullLoader)
except Exception:
    pass

# ---------------------------
# 10) Temp files insecure
# ---------------------------
tmp = "/tmp/secret_test.txt"
f = open(tmp, "w")                # ❌ création fichier tmp sans permissions sûres (Bandit B108)
f.write("secret")
f.close()

# ---------------------------
# 11) Logging secrets
# ---------------------------
import logging
logging.basicConfig(level=logging.DEBUG)
logging.debug("DEBUG: DB_PASSWORD = %s", DB_PASSWORD)   # ❌ fuite possible de secret dans logs

# ---------------------------
# 12) Use of environment variables printed
# ---------------------------
print(os.environ.get("SECRET_KEY"))

if __name__ == "__main__":
    # Ne pas exécuter en prod — ce script est uniquement pour tests SAST
    app.run(host="0.0.0.0", port=5000)

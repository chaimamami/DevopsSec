# vuln_test_semgrep.py
# Fichier volontairement vulnérable — pour démonstration SAST
import os
import subprocess
import pickle
import sqlite3
import requests
import flask
import hashlib
import yaml
import tempfile
import logging

# 1) Hardcoded "secret"
API_KEY = "AKIAAAAAAAAAAAAAAAAA"        # secret codé en dur

# 2) Command injection via concat
user_file = input("Entrez un chemin de fichier: ")
os.system("cat " + user_file)            # command injection

# 3) shell=True usage
subprocess.call("ls -la /tmp", shell=True)

# 4) Insecure deserialization
malformed = b"cos\nsystem\n(S'ls'\ntR."
pickle.loads(malformed)

# 5) SQL injection (string interpolation)
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
username = input("Username: ")
query = f"SELECT * FROM users WHERE name = '{username}'"
cursor.execute(query)

# 6) Dangerous eval
user_code = input("Entrez du code python: ")
eval(user_code)

# 7) Flask debug & reflected user input (XSS)
app = flask.Flask(__name__)
app.debug = True

@app.route("/hello")
def hello():
    name = flask.request.args.get("name", "visiteur")
    return "<h1>Bonjour " + name + "</h1>"

# 8) Ignoring SSL verification
requests.get("https://example.com/api", verify=False)

# 9) Weak hashing (MD5)
pwd = "mon_mot_de_passe"
print("MD5:", hashlib.md5(pwd.encode()).hexdigest())

# 10) Unsafe YAML load (legacy API)
yaml.load("!!python/object/apply:os.system ['echo vuln']")

# 11) Insecure temp file handling
tmp = "/tmp/secret_test.txt"
f = open(tmp, "w")
f.write("secret")
f.close()

# 12) Logging secrets
logging.basicConfig(level=logging.DEBUG)
logging.debug("DEBUG API_KEY=%s", API_KEY)

# 13) Print environment secrets
print(os.environ.get("SECRET_KEY"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

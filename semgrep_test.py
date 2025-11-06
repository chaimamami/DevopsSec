# test_semgrep.py — version corrigée
import os
import subprocess
import sqlite3
from pathlib import Path
from flask import Flask, request, jsonify

# Secret from environment (never commit real secrets)
API_KEY = os.environ.get("DEMO_API_KEY", None)

def safe_cat(filename: str) -> str:
    # Use Path to avoid weird paths and run subprocess with args (no shell)
    p = Path(filename).name  # keep only basename to avoid directory traversal
    result = subprocess.run(["cat", p], capture_output=True, text=True)
    return result.stdout

def get_user_by_name(db_path: str, username: str):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    # Parameterized query -> prevents SQL injection
    cur.execute("SELECT * FROM users WHERE name = ?", (username,))
    rows = cur.fetchall()
    conn.close()
    return rows

# Flask app (debug False in Jenkins / production)
app = Flask(__name__)
app.debug = False

@app.route("/test", methods=["GET"])
def test():
    return jsonify({"status": "ok"})

# small CLI examples (safe)
if __name__ == "__main__":
    # Example: don't call unsafe functions with attacker input in real apps
    # filename = input("Enter filename: ")
    # print(safe_cat(filename))

    # Example DB usage
    # username = input("Username: ")
    # print(get_user_by_name("users.db", username))

    print("File ready. Set DEMO_API_KEY env var to use API key.")

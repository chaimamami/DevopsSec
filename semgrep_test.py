# semgrep.py

import sqlite3

# Exemple de vulnérabilité : Injection SQL
def login(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"  # Vulnérabilité : Injection SQL
    cursor.execute(query)
    user = cursor.fetchone()
    if user:
        print("Login successful")
    else:
        print("Invalid credentials")
    conn.close()

# Exemple de vulnérabilité : Exécution de code arbitraire avec exec()
user_input = "print('Hello from exec!')"
exec(user_input)  # Vulnérabilité : Exécution de code arbitraire

# Exemple de vulnérabilité : Utilisation de données non validées dans un fichier
file_name = input("Enter file name: ")
with open(file_name, "r") as file:
    print(file.read())  # Vulnérabilité : Non validation de l'entrée utilisateur pour le chemin du fichier


import json
import requests
from datetime import datetime
import os

# Charger les rapports JSON de Semgrep et Trivy
with open("semgrep_report.json") as f:
    semgrep = json.load(f)

with open("trivy_report.json") as f:
    trivy = json.load(f)

# Compter les vulnérabilités
semgrep_vulns = len(semgrep.get("results", []))
trivy_vulns = len(trivy.get("Results", []))

# Récupérer l’URL du webhook Slack depuis Jenkins (variable d'environnement sécurisée)
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

# Créer le message à envoyer
message = {
    "text": f"""
*🛡️ DevSecOps Pipeline Report - {datetime.now().strftime("%Y-%m-%d %H:%M")}*

📘 *Semgrep Findings:* {semgrep_vulns}
📦 *Trivy Vulnerabilities:* {trivy_vulns}

{"✅ Aucun problème critique détecté" if semgrep_vulns + trivy_vulns == 0 else "⚠️ Des vulnérabilités nécessitent une attention immédiate."}
"""
}

# Envoyer la notification vers Slack
response = requests.post(SLACK_WEBHOOK_URL, json=message)
if response.status_code == 200:
    print("✅ Notification envoyée à Slack avec succès !")
else:
    print(f"❌ Erreur Slack : {response.status_code}, {response.text}")

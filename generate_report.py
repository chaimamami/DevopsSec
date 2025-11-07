import json
from datetime import datetime

# Charger les rapports existants
with open("semgrep_report.json", "r") as f:
    semgrep = json.load(f)
with open("trivy_report.json", "r") as f:
    trivy = json.load(f)

# Créer le rapport HTML combiné
html_content = f"""
<html>
<head><title>DevSecOps Security Report</title></head>
<body style="font-family:Arial;background:#1e1e1e;color:white;padding:20px;">
<h1>🛡️ DevSecOps Security Report</h1>
<p>Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

<h2>📘 Semgrep Findings</h2>
<pre style="background:#2d2d2d;padding:10px;">{json.dumps(semgrep, indent=2)}</pre>

<h2>📦 Trivy Vulnerabilities</h2>
<pre style="background:#2d2d2d;padding:10px;">{json.dumps(trivy, indent=2)}</pre>

</body></html>
"""

with open("devsecops_report.html", "w") as f:
    f.write(html_content)

print("✅ Rapport généré : devsecops_report.html")

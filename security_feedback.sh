#!/bin/bash
echo "🚫 Commit bloqué par le système de sécurité."
echo "🧠 Conseils pour corriger :"
echo "  • Ne laisse pas de mots de passe ou clés API dans le code."
echo "  • Utilise HTTPS au lieu de HTTP pour les requêtes réseau."
echo "  • Évite les fonctions dangereuses (os.system, eval, etc.)."
echo "  • Corrige les alertes ESLint et Semgrep avant de revalider."
echo "✅ Quand tout est corrigé : git add . && git commit -m 'fix: secure code'"

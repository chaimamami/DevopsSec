DevSecOps Security Pipeline – Demo_SAST
Description du projet

Ce projet met en place un pipeline DevSecOps complet exécuté dans une machine virtuelle Vagrant.
L’objectif est d’intégrer la sécurité à chaque étape du cycle de développement logiciel, depuis l’analyse du code jusqu’au déploiement et à la supervision.

Le pipeline est entièrement automatisé à l’aide de Jenkins et combine plusieurs outils d’analyse (SAST, SCA, DAST) ainsi que des outils de monitoring pour assurer une visibilité continue sur la qualité et la sécurité du code.


Architecture du pipeline

Le pipeline Jenkins est structuré en plusieurs étapes successives :

Checkout SCM : récupération du code source depuis GitHub.

Build et Tests : installation des dépendances et exécution de tests unitaires.

SAST (Static Application Security Testing) :

ESLint pour la détection d’erreurs et failles dans le code JavaScript.

Semgrep pour l’analyse statique des fichiers Python et JS.

SCA (Software Composition Analysis) :

Trivy pour identifier les vulnérabilités dans les dépendances logicielles.

Secret Scanning :

Gitleaks pour détecter les clés API ou mots de passe exposés dans le code.

Docker Build et Scan :

Construction de l’image Docker et analyse de sécurité avec Trivy.

Analyse statique avec SonarQube :

Évaluation de la qualité du code et détection des vulnérabilités.

DAST (Dynamic Application Security Testing) :

OWASP ZAP pour simuler des attaques sur l’application en exécution.

Monitoring et Reporting :

Export des résultats vers Prometheus.

Visualisation des métriques dans Grafana.

Notification automatique des résultats dans Slack.

Résultats obtenus

Génération automatique de rapports JSON pour ESLint, Semgrep, Trivy et OWASP ZAP.

Création d’un fichier security_metrics.prom contenant les métriques principales, lu par Prometheus.

Visualisation en temps réel dans Grafana :

Taux d’utilisation CPU et mémoire du pipeline.

Nombre d’erreurs ESLint et findings Semgrep.

Vulnérabilités critiques et hautes détectées par Trivy.

Notification automatique sur Slack à chaque exécution du pipeline avec résumé des résultats.







Objectif pédagogique

Le but du projet est de démontrer comment intégrer la sécurité dans toutes les étapes d’un pipeline CI/CD.
Chaque commit sur GitHub déclenche automatiquement une analyse complète du code, des dépendances et des conteneurs afin de renforcer la qualité et la conformité du projet.











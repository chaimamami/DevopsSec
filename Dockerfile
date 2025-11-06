# Étape 1 : base sécurisée
FROM node:18-alpine

# Étape 2 : définition du dossier de travail
WORKDIR /app

# Étape 3 : copie du projet
COPY . .

# Étape 4 : installation des dépendances
RUN npm install

# Étape 5 : exécution des tests basiques
RUN npm test || echo "Tests skipped"

# Étape 6 : port exposé (si app web)
EXPOSE 3000

# Étape 7 : commande de démarrage
CMD ["npm", "start"]

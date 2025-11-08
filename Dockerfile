# Étape 1 : utiliser une image Node légère et sécurisée
FROM node:18-alpine

# Définir le dossier de travail
WORKDIR /app

# Copier les fichiers de configuration et dépendances
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier le reste du code source
COPY . .

# Exposer le port d’exécution
EXPOSE 3000

# Créer un utilisateur non-root pour plus de sécurité
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Changer d'utilisateur
USER appuser

# Démarrer l’application
CMD ["npm", "start"]

const express = require('express');
const app = express();
const PORT = 3000;

// Route principale
app.get('/', (req, res) => {
  res.send('✅ Application demo-sast en marche !');
});

// Lancer le serveur
app.listen(PORT, () => {
  console.log(`🚀 Serveur démarré sur le port ${PORT}`);
});

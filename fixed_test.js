// fixed_test.js
// version corrigée : let/const, validate input, no exec with untrusted input
const express = require('express');
const app = express();
const { execFile } = require('child_process');
const path = require('path');

app.get('/greet', (req, res) => {
  const name = req.query.name || 'visiteur';
  // échappement simple et usage de template literals
  const safeName = String(name).replace(/[<>]/g, '');
  res.send(`<h1>Hello ${safeName}</h1>`);
});

app.get('/run', (req, res) => {
  // validation stricte du paramètre et utilisation d'execFile avec fichier autorisé
  const requested = req.query.file;
  const allowedDir = '/tmp';
  if (!requested) return res.status(400).send('file required');
  const resolved = path.resolve(allowedDir, requested);
  if (!resolved.startsWith(allowedDir)) return res.status(403).send('forbidden');

  execFile('ls', ['-la', resolved], (err, stdout, stderr) => {
    if (err) return res.status(500).send('error');
    res.send(`<pre>${stdout}</pre>`);
  });
});

app.listen(3000, () => console.log('listening on 3000'));

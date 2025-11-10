// Exemple de code vulnérable pour ESLint
let password = "123456";  // hardcoded secret
eval("console.log('XSS!')");  // utilisation dangereuse d'eval

function login(user) {
    console.log("User logged in: " + user); // problème de log d'informations sensibles
}
login("admin");

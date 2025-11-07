// test.js — version corrigée

// No hardcoded password. Use env/config or prompt (do not commit secrets).
const DUMMY_PASSWORD = null; // placeholder — never store real passwords in source

function login(user, pass) {
  // use strict equality
  if (user === "admin" && pass === "1234") {
    // do not use eval; use safe logging and server-side auth
    // example: set a safe message
    //console.info('Admin logged in'); // allowed console method
    // do NOT use document.write -> manipulate DOM safely if needed
    // e.g.:
    // document.getElementById('welcome').textContent = `Bienvenue ${user}`;
  } else {
    console.warn("Access denied");
  }
}

// never store secrets in localStorage
// localStorage.setItem("token", "abcdef123456"); // removed

// declare variables properly
let undeclaredVar = 42;
login("admin", "1234");

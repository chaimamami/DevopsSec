export default [
  {
    files: ["**/*.js"],
    languageOptions: {
      ecmaVersion: 2021,
      sourceType: "module"
    },
    rules: {
      "no-var": "error",
      "no-console": ["warn", { "allow": ["warn", "error"] }]
    }
  }
];

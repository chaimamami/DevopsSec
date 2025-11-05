// ✅ Secure version — no hardcoded password

// Load password from environment variable instead of hardcoding it
const password = process.env.ADMIN_PASSWORD || "undefined";

// Never print the actual password to logs


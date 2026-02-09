/**
 * Setup Environment Variables Script
 * 
 * This script helps create a .env file from .env.example
 * Run: node scripts/setup-env.js
 */

const fs = require('fs');
const path = require('path');

const envExamplePath = path.join(__dirname, '..', '.env.example');
const envPath = path.join(__dirname, '..', '.env');

if (fs.existsSync(envPath)) {
  console.log('✅ .env file already exists');
  console.log('📝 If you need to update it, edit .env manually');
  process.exit(0);
}

if (!fs.existsSync(envExamplePath)) {
  console.error('❌ .env.example file not found');
  process.exit(1);
}

// Read .env.example
const envExample = fs.readFileSync(envExamplePath, 'utf8');

// Create .env from .env.example
fs.writeFileSync(envPath, envExample);

console.log('✅ Created .env file from .env.example');
console.log('⚠️  Please update the values in .env with your actual credentials:');
console.log('   - DATABASE_URL: Your Neon PostgreSQL connection string');
console.log('   - BETTER_AUTH_SECRET: A random secret (at least 32 characters)');
console.log('   - BETTER_AUTH_URL: Your app URL (usually http://localhost:3000)');
console.log('   - NEXT_PUBLIC_BETTER_AUTH_URL: Same as BETTER_AUTH_URL');

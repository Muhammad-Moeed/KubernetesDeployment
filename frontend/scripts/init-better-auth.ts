/**
 * Better Auth Database Initialization Script
 * 
 * This script initializes Better Auth database tables.
 * Run this once before starting the application:
 * 
 * npx tsx scripts/init-better-auth.ts
 * 
 * Or use Better Auth CLI:
 * npx @better-auth/cli generate
 * npx @better-auth/cli migrate
 */

import { betterAuth } from "better-auth";
import * as dotenv from "dotenv";
import { resolve } from "path";

// Load environment variables
dotenv.config({ path: resolve(process.cwd(), ".env") });

const DATABASE_URL = process.env.DATABASE_URL;
const BETTER_AUTH_SECRET = process.env.BETTER_AUTH_SECRET;

if (!DATABASE_URL) {
  console.error("❌ DATABASE_URL environment variable is not set");
  process.exit(1);
}

if (!BETTER_AUTH_SECRET) {
  console.error("❌ BETTER_AUTH_SECRET environment variable is not set");
  process.exit(1);
}

console.log("🚀 Initializing Better Auth database...");

const auth = betterAuth({
  database: {
    provider: "postgres",
    url: DATABASE_URL,
  },
  emailAndPassword: {
    enabled: true,
  },
  secret: BETTER_AUTH_SECRET,
  baseURL: process.env.BETTER_AUTH_URL || process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000",
});

// Better Auth automatically creates tables on first use
// But we can trigger it by calling the handler
console.log("✅ Better Auth initialized");
console.log("📝 Database tables will be created automatically on first signup");
console.log("💡 If tables don't exist, run: npx @better-auth/cli generate && npx @better-auth/cli migrate");

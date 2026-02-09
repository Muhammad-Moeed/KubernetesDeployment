import { defineConfig } from "@better-auth/cli";
import * as dotenv from "dotenv";
import { resolve } from "path";

// Load environment variables
dotenv.config({ path: resolve(__dirname, ".env") });

const DATABASE_URL = process.env.DATABASE_URL;
const BETTER_AUTH_SECRET = process.env.BETTER_AUTH_SECRET;

if (!DATABASE_URL) {
  throw new Error("DATABASE_URL is required in .env file");
}

if (!BETTER_AUTH_SECRET) {
  throw new Error("BETTER_AUTH_SECRET is required in .env file");
}

export default defineConfig({
  database: {
    provider: "postgres",
    url: DATABASE_URL,
  },
  secret: BETTER_AUTH_SECRET,
});

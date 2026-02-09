/**
 * JWT Token Generation Utility
 * Generates JWT tokens compatible with FastAPI backend
 * Uses the same BETTER_AUTH_SECRET as Better Auth for consistency
 */

import { SignJWT } from "jose";

const BETTER_AUTH_SECRET = process.env.BETTER_AUTH_SECRET || "";

if (!BETTER_AUTH_SECRET) {
  console.warn("⚠️  BETTER_AUTH_SECRET is not set. JWT generation will fail.");
}

/**
 * Generate a JWT token for FastAPI backend
 * @param userId - User ID from Better Auth session
 * @param email - User email from Better Auth session (optional)
 * @param name - User name from Better Auth session (optional)
 * @param expiresIn - Token expiration time in seconds (default: 24 hours)
 * @returns JWT token string
 */
export async function generateJWTToken(
  userId: string,
  email?: string,
  name?: string,
  expiresIn: number = 60 * 60 * 24 // 24 hours
): Promise<string> {
  if (!BETTER_AUTH_SECRET) {
    throw new Error("BETTER_AUTH_SECRET is not configured");
  }

  const secret = new TextEncoder().encode(BETTER_AUTH_SECRET);
  const now = Math.floor(Date.now() / 1000);

  const token = await new SignJWT({
    // JWT payload - FastAPI expects user_id in these fields
    sub: userId, // Standard JWT subject claim
    userId: userId, // Alternative field
    user_id: userId, // Another alternative
    id: userId, // Simple ID field
    email: email || null, // User email
    name: name || null, // User name
    iat: now, // Issued at
  })
    .setProtectedHeader({ alg: "HS256" })
    .setIssuedAt(now)
    .setExpirationTime(now + expiresIn)
    .setSubject(userId)
    .sign(secret);

  return token;
}

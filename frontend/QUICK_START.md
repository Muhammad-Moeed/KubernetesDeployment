# Quick Start Guide - Better Auth Setup

## Step 1: Update Environment Variables

The `.env` file has been created. **You MUST update it with your actual values:**

1. Open `frontend/.env`
2. Update these values:

```env
# Your Neon PostgreSQL connection string
DATABASE_URL=postgresql://user:password@host:port/database?sslmode=require

# Generate a random secret (at least 32 characters)
# You can use: openssl rand -base64 32
BETTER_AUTH_SECRET=your-random-secret-here-min-32-chars

# Your app URL
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000

# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Step 2: Verify Database Connection

Make sure your `DATABASE_URL` is correct and the database is accessible.

## Step 3: Start the Development Server

```bash
cd frontend
npm run dev
```

## Step 4: Test Signup

1. Go to http://localhost:3000/signup
2. Create a new account
3. Better Auth will automatically create database tables on first signup

## Troubleshooting

### Error: 500 Internal Server Error

**Check the terminal/console for detailed error messages.**

Common issues:

1. **Database Connection Failed**
   - Verify `DATABASE_URL` is correct
   - Check if database is accessible
   - Ensure SSL mode is enabled (`?sslmode=require`)

2. **Missing Environment Variables**
   - Ensure `.env` file exists in `frontend` directory
   - Restart dev server after changing `.env`
   - Check that all required variables are set

3. **Better Auth Secret Too Short**
   - Must be at least 32 characters
   - Generate a new one: `openssl rand -base64 32`

4. **Database Tables Not Created**
   - Better Auth creates tables automatically on first signup
   - If issues persist, manually create tables:
     ```bash
     npm install -D @better-auth/cli
     npx @better-auth/cli generate
     npx @better-auth/cli migrate
     ```

## What Happens on Signup

1. User submits email and password
2. Better Auth validates input
3. Password is hashed
4. User record is created in database
5. Session is created
6. User is logged in automatically

## Database Tables

Better Auth automatically creates these tables:
- `user` - User accounts
- `session` - Active sessions
- `account` - OAuth accounts (if using OAuth)
- `verification` - Email verification tokens

**You don't need to create these manually!**

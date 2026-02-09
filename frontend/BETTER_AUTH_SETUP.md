# Better Auth Setup Guide

## Prerequisites

1. **Environment Variables**: Create a `.env` file in the `frontend` directory with:

```env
# Database Configuration
DATABASE_URL=postgresql://user:password@host:port/database?sslmode=require

# Better Auth Configuration
BETTER_AUTH_SECRET=your-secret-key-min-32-characters-long
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000

# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Database Setup

Better Auth automatically creates the required database tables on first use. However, if you want to manually create them:

### Option 1: Using Better Auth CLI (Recommended)

```bash
# Install Better Auth CLI
npm install -D @better-auth/cli

# Generate database schema
npx @better-auth/cli generate

# Apply migrations
npx @better-auth/cli migrate
```

### Option 2: Automatic (Default)

Better Auth will automatically create tables when the first user signs up. No manual migration needed!

## Verification

1. **Check Database Connection**:
   - Ensure your `DATABASE_URL` is correct
   - Test connection to Neon PostgreSQL database

2. **Check Environment Variables**:
   - All required variables are set in `.env`
   - `BETTER_AUTH_SECRET` is at least 32 characters

3. **Start Development Server**:
   ```bash
   npm run dev
   ```

4. **Test Signup**:
   - Go to http://localhost:3000/signup
   - Create a new account
   - Check database for new user record

## Troubleshooting

### Error: 500 Internal Server Error on Signup

1. **Check Database Connection**:
   - Verify `DATABASE_URL` is correct
   - Ensure database is accessible
   - Check SSL mode is set correctly

2. **Check Environment Variables**:
   - Ensure `.env` file exists in `frontend` directory
   - Restart dev server after changing `.env`

3. **Check Better Auth Secret**:
   - Must be at least 32 characters
   - Should be a random string

4. **Check Database Tables**:
   - Better Auth creates tables automatically
   - If tables don't exist, run: `npx @better-auth/cli migrate`

### Error: Database connection failed

- Verify your Neon PostgreSQL connection string
- Check if database exists
- Ensure SSL mode is enabled (`?sslmode=require`)

## Database Tables Created by Better Auth

Better Auth automatically creates these tables:
- `user` - User accounts
- `session` - User sessions
- `account` - OAuth accounts (if using OAuth)
- `verification` - Email verification tokens

You don't need to create these manually - Better Auth handles it!

# Database Setup for Better Auth

## Quick Setup (Recommended)

Better Auth should automatically create tables on first signup. However, if you're getting errors, you can manually create the tables.

## Option 1: Manual SQL Script (Fastest)

1. Open your Neon PostgreSQL dashboard
2. Go to SQL Editor
3. Copy and paste the contents of `scripts/create-better-auth-tables.sql`
4. Run the script

This will create all required tables for Better Auth.

## Option 2: Using Better Auth CLI

```bash
cd frontend

# Make sure .env file exists with DATABASE_URL and BETTER_AUTH_SECRET
# Then run:
npx @better-auth/cli generate
npx @better-auth/cli migrate
```

## Option 3: Let Better Auth Auto-Create (Default)

Better Auth will automatically create tables when you make the first signup request. Just ensure:
- ✅ DATABASE_URL is correct in .env
- ✅ BETTER_AUTH_SECRET is set (at least 32 characters)
- ✅ Database is accessible

## Verify Tables

After setup, you should have these tables:
- `user` - User accounts
- `session` - Active sessions  
- `account` - OAuth accounts (if using OAuth)
- `verification` - Email verification tokens

## Troubleshooting

### Error: "Failed to initialize database adapter"

1. **Check Database Connection**:
   - Verify DATABASE_URL is correct
   - Test connection in Neon dashboard
   - Ensure SSL mode is enabled (`?sslmode=require`)

2. **Check Environment Variables**:
   - Ensure .env file exists in `frontend` directory
   - Restart dev server after changing .env

3. **Manual Table Creation**:
   - Use the SQL script in `scripts/create-better-auth-tables.sql`
   - Run it directly in Neon PostgreSQL dashboard

### Error: "Table does not exist"

Run the SQL script manually or let Better Auth create tables automatically on first signup.

# Deployment Environment Variables

## Required Environment Variables for Production

Deploy karte waqt ye environment variables set karein:

### Frontend (Vercel/Netlify/etc.)

```env
# Backend API URL (Production)
NEXT_PUBLIC_API_URL=https://your-backend-api.com

# Database (if using Better Auth in future)
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=your-secret-key

# Auth URLs (if using Better Auth in future)
BETTER_AUTH_URL=https://your-frontend-domain.com
NEXT_PUBLIC_BETTER_AUTH_URL=https://your-frontend-domain.com
```

### Important Notes:

1. **API Client**: 
   - Uses `NEXT_PUBLIC_API_URL` environment variable
   - Production mein apne backend URL ko set karein
   - Default: `http://localhost:8000` (sirf development ke liye)

2. **JWT Token Endpoint**:
   - Uses relative URL `/api/auth/jwt-token`
   - Automatically current domain use karta hai
   - Production mein hosted URL se kaam karega ✅

3. **Login/Signup**:
   - Currently using mock auth (localStorage)
   - No external API calls
   - Cookies use relative paths ✅

4. **All Fetch Calls**:
   - JWT token: Relative URL ✅
   - API calls: Environment variable se ✅
   - No hardcoded localhost URLs ✅

## Verification Checklist:

- ✅ API Client uses `NEXT_PUBLIC_API_URL` env var
- ✅ JWT endpoint uses relative URL
- ✅ No hardcoded localhost URLs in production code
- ✅ Cookies use relative paths
- ✅ All redirects use relative paths

## Deployment Steps:

1. Set `NEXT_PUBLIC_API_URL` to your production backend URL
2. Deploy frontend
3. All requests will automatically use production URLs

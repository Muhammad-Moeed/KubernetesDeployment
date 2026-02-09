# 🚀 Frontend Deployment Guide - Vercel

## ✅ Backend Already Deployed
Backend URL: `https://moeed497-chatbot-phase3.hf.space`

---

## 📋 Pre-Deployment Checklist

### 1. Backend URL Updated ✅
- [x] `.env` updated with Hugging Face backend URL
- [x] `.env.production` created for production deployment
- [x] Backend CORS already allows all origins

### 2. Environment Variables Ready ✅
```env
NEXT_PUBLIC_API_URL=https://moeed497-chatbot-phase3.hf.space
BETTER_AUTH_SECRET=oalcVJgkt7LeyeGJ1mvZ5Kv9xcX4xh92
DATABASE_URL=postgresql://neondb_owner:npg_JlBaIg8bEjX1@ep-ancient-star-a7nixeys-pooler.ap-southeast-2.aws.neon.tech/neondb?sslmode=require
```

---

## 🚀 Deploy to Vercel

### Option 1: Via Vercel Dashboard (Recommended)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Updated backend URL for production"
   git push origin main
   ```

2. **Vercel Dashboard**
   - Go to [vercel.com/new](https://vercel.com/new)
   - Import your GitHub repository
   - Root Directory: Select `frontend`
   - Framework Preset: Next.js (auto-detected)

3. **Environment Variables**
   Add these in Vercel dashboard:
   ```
   NEXT_PUBLIC_API_URL = https://moeed497-chatbot-phase3.hf.space
   BETTER_AUTH_SECRET = oalcVJgkt7LeyeGJ1mvZ5Kv9xcX4xh92
   DATABASE_URL = postgresql://neondb_owner:npg_JlBaIg8bEjX1@ep-ancient-star-a7nixeys-pooler.ap-southeast-2.aws.neon.tech/neondb?sslmode=require
   ```

4. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes
   - Get your URL: `https://your-app.vercel.app`

---

### Option 2: Via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to frontend folder
cd frontend

# Login to Vercel
vercel login

# Deploy
vercel --prod

# Follow prompts and add environment variables when asked
```

---

## ⚙️ Post-Deployment Steps

### 1. Update Frontend URL (If needed)
After deployment, if you need to update backend CORS or Better Auth URLs:

**Backend `.env`** (on Hugging Face):
```env
FRONTEND_URL=https://your-app.vercel.app
```

**Frontend `.env.production`** (on Vercel):
```env
BETTER_AUTH_URL=https://your-app.vercel.app
NEXT_PUBLIC_BETTER_AUTH_URL=https://your-app.vercel.app
```

### 2. Test Deployment
- Visit your Vercel URL
- Open browser console (F12)
- Login with test account
- Check console logs:
  ```
  🔑 Getting JWT token for: test@example.com user_id: user_xxx
  📋 Fetching tasks for user_id: user_xxx
  ✅ Fetched X tasks from database
  ```
- Create a task
- Logout and relogin
- Verify tasks persist ✅

---

## 🐛 Troubleshooting

### Issue: CORS Error
**Solution**: Backend already has `allow_origins=["*"]` - should work fine

### Issue: 502 Bad Gateway
**Check**:
- Backend URL correct? `https://moeed497-chatbot-phase3.hf.space`
- Backend is running? Test: Visit backend URL directly
- Hugging Face Space is not sleeping? (Free tier sleeps after inactivity)

### Issue: Tasks not persisting
**Check**:
- Database URL correct in environment variables
- Console logs show same user_id on relogin
- Check `localStorage.getItem("users_map")` in browser console

### Issue: Environment variables not working
**Solution**: 
- Redeploy after adding env vars
- Or use Vercel CLI: `vercel env pull`

---

## 🎯 Quick Test Commands

```javascript
// Test in browser console after deployment:

// 1. Check backend connection
fetch('https://moeed497-chatbot-phase3.hf.space/health')
  .then(r => r.json())
  .then(d => console.log('Backend:', d));

// 2. Check user_id mapping
const usersMap = JSON.parse(localStorage.getItem("users_map") || "{}");
console.log("Users Map:", usersMap);

// 3. Check current session
const session = JSON.parse(localStorage.getItem("session"));
console.log("Session user_id:", session?.user?.id);
```

---

## 📝 Important Notes

1. **Backend URL Updated**: ✅ Already done in `.env` and `.env.production`
2. **CORS Configured**: ✅ Backend allows all origins
3. **Database Connection**: ✅ Same Neon PostgreSQL database
4. **User Persistence**: ✅ Uses `users_map` in localStorage
5. **Real-time Sync**: ✅ All data from database, not localStorage

---

## 🎉 Deployment Complete!

After deployment:
1. ✅ Frontend deployed on Vercel
2. ✅ Backend running on Hugging Face
3. ✅ Database on Neon PostgreSQL
4. ✅ Users can login, create tasks, logout, relogin
5. ✅ Tasks persist across sessions
6. ✅ Real-time data from database

**Your app is live!** 🚀

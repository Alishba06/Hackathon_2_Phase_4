# Authentication 401 Error Fix

## Problem
You were getting a 401 Unauthorized error when trying to fetch tasks:
```
Error: Request failed with status code 401
Authentication error: Please log in to access tasks.
```

## What Was Fixed

### 1. Updated `src/app/page.tsx`
- Added authentication check before fetching tasks
- The homepage now only fetches tasks if the user is authenticated
- Unauthenticated users see a friendly "No tasks yet" message instead of an error

### 2. Updated `src/lib/auth/tokenUtils.ts`
- Token is now stored in **both cookies AND localStorage** for better compatibility
- `getToken()` now checks cookies first, then falls back to localStorage
- This ensures the API client can always find the authentication token

## How to Use the Application

### Step 1: Start the Backend
Make sure your FastAPI backend is running:
```bash
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Step 2: Start the Frontend
The frontend should already be running at:
```
http://localhost:3000
```

### Step 3: Sign In or Sign Up
1. Navigate to `http://localhost:3000/sign-in`
2. If you don't have an account, click "Sign Up" and create one
3. Enter your email and password
4. Click "Sign In"

### Step 4: Access Dashboard
After successful login:
- You'll be redirected to `/dashboard`
- The token is automatically stored in cookies and localStorage
- All API requests will now include the authentication token
- You can view, create, update, and delete tasks

## How Authentication Works

1. **Login**: When you sign in, the backend returns a JWT token
2. **Storage**: The token is stored in:
   - Cookies (for server-side requests)
   - localStorage (for client-side requests)
3. **API Requests**: The API client automatically attaches the token to every request:
   ```
   Authorization: Bearer <your-jwt-token>
   ```
4. **Backend Verification**: The backend verifies the token and returns user-specific data

## Troubleshooting

### Still getting 401 errors?

1. **Check if you're logged in**
   - Open browser DevTools (F12)
   - Go to Application → Cookies → http://localhost:3000
   - Look for `jwt_token` cookie
   - If missing, sign in again

2. **Check backend is running**
   - Open `http://127.0.0.1:8000/docs` in your browser
   - You should see the Swagger API documentation
   - If not, start the backend

3. **Clear old tokens and re-login**
   ```javascript
   // Run in browser console
   localStorage.removeItem('jwt_token');
   document.cookie = 'jwt_token=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/';
   // Then sign in again
   ```

4. **Check network requests**
   - Open DevTools → Network tab
   - Try to access dashboard
   - Look for failed requests (red)
   - Check the Authorization header is present

## Files Modified

- `frontend/src/app/page.tsx` - Fixed homepage to handle unauthenticated state
- `frontend/src/lib/auth/tokenUtils.ts` - Added localStorage fallback for token storage

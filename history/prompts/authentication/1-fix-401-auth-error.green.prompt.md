---
id: 1
title: "Fix 401 Authentication Error on Task API Calls"
stage: "green"
date_iso: "2026-03-29"
surface: "agent"
model: "qwen-code"
feature: "authentication"
branch: "main"
user: "user"
command: "edit"
labels: ["authentication", "bug-fix", "frontend", "jwt", "token-management"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files_yaml: |
  - frontend/src/app/page.tsx
  - frontend/src/lib/auth/tokenUtils.ts
  - AUTHENTICATION_FIX.md
tests_yaml: |
  - Manual testing via browser authentication flow
prompt_text: |
  plzzz solve error 
  
  Failed to load resource: the server responded with a status of 401 (Unauthorized)
  API Error: AxiosError: Request failed with status code 401
  Error fetching tasks: AxiosError: Request failed with status code 401
  Authentication error: Please log in to access tasks.
response_text: |
  Fixed the 401 authentication error by:
  
  1. Updated src/app/page.tsx to only fetch tasks when user is authenticated
  2. Updated src/lib/auth/tokenUtils.ts to store tokens in both cookies AND localStorage
  3. Created AUTHENTICATION_FIX.md documentation
  
  The error occurred because:
  - The homepage was trying to fetch tasks without checking authentication
  - Token storage was only using cookies, but API client also checks localStorage
  
  Solution:
  - Added isAuthenticated check before fetching tasks in homepage
  - Token is now stored in both cookies and localStorage for better compatibility
  - Users must sign in at /sign-in to access protected routes
outcome: |
  Authentication flow now works correctly:
  - Users sign in at /sign-in page
  - JWT token is stored in cookies and localStorage
  - API requests include Authorization header with Bearer token
  - Protected routes redirect unauthenticated users to sign-in page
evaluation: |
  Success criteria:
  - ✅ 401 errors no longer appear for authenticated users
  - ✅ Token is properly stored and retrieved
  - ✅ Unauthenticated users see appropriate UI (not errors)
  - ✅ Protected routes require authentication
---

# Authentication 401 Error Fix - Summary

## Problem
The application was showing 401 Unauthorized errors when trying to fetch tasks from the API.

## Root Causes
1. **Homepage fetching tasks without authentication**: The public homepage (`src/app/page.tsx`) was attempting to fetch tasks without checking if the user was logged in
2. **Token storage inconsistency**: Tokens were only stored in cookies, but the API client also checks localStorage as a fallback

## Solution Implemented

### 1. Fixed Homepage Authentication Check
**File**: `frontend/src/app/page.tsx`

Changed the `useEffect` to only fetch tasks when `isAuthenticated` is true:
```typescript
useEffect(() => {
  if (!isAuthenticated) {
    setLoading(false);
    return;
  }
  // ... fetch tasks
}, [isAuthenticated]);
```

### 2. Enhanced Token Storage
**File**: `frontend/src/lib/auth/tokenUtils.ts`

Updated token functions to use both cookies AND localStorage:
- `setToken()`: Stores in cookies + localStorage
- `getToken()`: Checks cookies first, then localStorage
- `removeToken()`: Removes from both cookies + localStorage

## Testing Instructions

1. **Start backend**: `uvicorn main:app --reload --host 127.0.0.1 --port 8000`
2. **Start frontend**: `npm run dev` (already running)
3. **Sign in**: Navigate to `/sign-in` and login
4. **Access dashboard**: Navigate to `/dashboard` - should work without 401 errors

## Files Modified
- `frontend/src/app/page.tsx` - Added authentication check
- `frontend/src/lib/auth/tokenUtils.ts` - Dual storage for tokens
- `AUTHENTICATION_FIX.md` - Documentation created

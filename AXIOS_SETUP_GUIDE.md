# Axios Setup Guide for Next.js Frontend

## Overview
This document explains how to properly configure Axios for your Next.js frontend to communicate with your FastAPI backend, addressing the network errors you were experiencing.

## Root Causes of Network Errors

1. **Missing API Endpoint**: The `/auth/me` endpoint was not implemented in the backend, causing the `getUser()` function to fail.
2. **Inconsistent API Calls**: The frontend was mixing fetch API and Axios calls, leading to inconsistent error handling and token management.
3. **Improper Token Handling**: The token was not being properly attached to all requests in a consistent way.

## Solution Summary

### Backend Changes Made
1. Added `/auth/me` endpoint to retrieve current user profile
2. Added `/auth/logout` endpoint for user logout functionality
3. Both endpoints properly validate JWT tokens and return user information

### Frontend Changes Made
1. Updated `api.ts` to use Axios consistently for all API calls
2. Implemented Axios interceptors for automatic token attachment and error handling
3. Updated `tokenUtils.ts` to use Axios with proper base URL configuration
4. Fixed the `getUser()` function to correctly parse the response

## Corrected Axios Configuration

### 1. API Service (`frontend/src/services/api.ts`)
```typescript
import axios from 'axios';
import { getToken } from './auth';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

// Configure axios defaults
axios.defaults.baseURL = API_BASE_URL;

// Add a request interceptor to include the token in all requests
axios.interceptors.request.use(
  (config) => {
    const token = getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add a response interceptor to handle errors globally
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Unauthorized - possibly token expired
      // Remove token and redirect to login (if in browser)
      if (typeof window !== 'undefined') {
        localStorage.removeItem('jwt_token');
      }
      // Optionally redirect to login page
      // window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Task API functions using Axios
export const getTasks = async (userId: string) => {
  try {
    const response = await axios.get(`/api/${userId}/tasks`);
    return response.data;
  } catch (error: any) {
    console.error('Get tasks failed:', error.response?.data || error.message);
    throw error;
  }
};

// ... other API functions
```

### 2. Authentication Utilities (`frontend/src/lib/auth/tokenUtils.ts`)
```typescript
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

// Get the current user profile
export const getUser = async () => {
  try {
    const token = isBrowser() ? localStorage.getItem('jwt_token') : null;
    if (!token) return null;

    const response = await axios.get('/auth/me', {
      baseURL: API_BASE_URL,
      headers: { Authorization: `Bearer ${token}` },
    });

    return response.data; // Return the full user data
  } catch (error: any) {
    console.error('Get user failed:', error);

    // Check if it's a network error
    if (error.code === 'ERR_NETWORK') {
      console.error('Network error: Could not connect to the server. Please make sure the backend is running.');
      return null; // Return null instead of removing the token in case of network error
    }

    if (isBrowser()) {
      localStorage.removeItem('jwt_token');
    }
    return null;
  }
};
```

## Step-by-Step Fix Instructions

1. **Start the Backend Server**:
   ```bash
   cd backend
   uvicorn src.main:app --reload --port 8000
   ```

2. **Start the Frontend Development Server**:
   ```bash
   cd frontend
   npm run dev
   ```

3. **Verify Environment Variables**:
   - Ensure `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000` is set in your `.env.local` file

4. **Test the Connection**:
   - Register a new user
   - Login with the registered user
   - Verify that the dashboard loads and `getUser()` function works properly

## Troubleshooting Common Issues

### Issue: Network Error After Login
**Solution**: Verify that the backend server is running on the correct port (8000 by default) and that the `NEXT_PUBLIC_API_BASE_URL` environment variable is correctly set.

### Issue: 401 Unauthorized Errors
**Solution**: Check that the JWT token is being properly stored in localStorage after login and that the `Authorization: Bearer <token>` header is being sent with each request.

### Issue: CORS Errors
**Solution**: Verify that the backend's `BACKEND_CORS_ORIGINS` environment variable includes your frontend's origin (typically `http://localhost:3000`).

## Testing the Connection

To verify everything is working properly, you can test the API endpoints directly:

1. **Login**: POST to `/auth/login` with username/password
2. **Get Profile**: GET to `/auth/me` with Authorization header
3. **Logout**: POST to `/auth/logout` with Authorization header
4. **Task Operations**: Various endpoints under `/api/{userId}/tasks/*`

## Conclusion

With these changes, your Next.js frontend should now properly communicate with your FastAPI backend using Axios. The network errors should be resolved, and the `getUser()` function should work correctly after login.
# Authentication and Routing Implementation Guide

This guide explains how to implement authentication and routing for your Next.js + FastAPI Todo App.

## 1. Login/Register Functions in AuthProvider.tsx

The AuthProvider now handles authentication state and token management:

```typescript
// frontend/src/providers/AuthProvider.tsx
import React, { createContext, useContext, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { getUser, signIn as signInUtil, signOut as signOutUtil, register as registerUser, removeToken, getToken } from '@/lib/auth/tokenUtils';

// Define the shape of our auth context
interface AuthContextType {
  user: any | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, firstName?: string, lastName?: string) => Promise<void>;
  logout: () => Promise<void>;
  isAuthenticated: boolean;
  handleTokenExpiration: () => void;
}

// Create the auth context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  // Check if user is authenticated on mount
  useEffect(() => {
    const checkAuth = async () => {
      try {
        // First check if we have a token
        const token = getToken();
        if (!token) {
          // No token means user is not authenticated
          setUser(null);
          setLoading(false);
          return;
        }

        // Token exists, try to get user data
        const userData = await getUser();
        setUser(userData);
      } catch (error: any) {
        console.error('Auth check failed:', error);

        // If auth check fails, remove the invalid token and set user to null
        removeToken();
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  // LOGIN FUNCTION
  const login = async (email: string, password: string) => {
    try {
      // Sign in and get token
      await signInUtil(email, password);

      // Fetch user profile using token
      const userData = await getUser();
      if (!userData) {
        throw new Error('Failed to fetch user profile after login.');
      }

      setUser(userData);

      // Redirect to dashboard after successful login
      router.push('/dashboard');
    } catch (error: any) {
      console.error('Login failed:', error);

      if (error.message?.includes('Network Error')) {
        alert('Could not connect to the server. Please make sure the backend is running.');
      }

      throw error;
    }
  };

  // REGISTER FUNCTION
  const register = async (email: string, password: string, firstName?: string, lastName?: string) => {
    try {
      // Register user and get token
      await registerUser(email, password, firstName, lastName);

      // Fetch user profile using token
      const userData = await getUser();
      if (!userData) {
        throw new Error('Failed to fetch user profile after registration.');
      }

      setUser(userData);

      // Redirect to dashboard after successful registration
      router.push('/dashboard');
    } catch (error: any) {
      console.error('Registration failed:', error);

      if (error.message?.includes('Network Error')) {
        alert('Could not connect to the server. Please make sure the backend is running.');
      }

      throw error;
    }
  };

  // LOGOUT FUNCTION
  const logout = async () => {
    try {
      await signOutUtil();
    } catch (error) {
      console.error('Logout failed:', error);
      // Even if the backend logout fails, clear local token and user data
      removeToken();
    } finally {
      setUser(null);
      router.push('/(auth)/sign-in'); // redirect to login
    }
  };

  // HANDLE TOKEN EXPIRATION
  const handleTokenExpiration = () => {
    setUser(null);
    removeToken(); // Use the new utility function
    router.push('/(auth)/sign-in');
  };

  const isAuthenticated = !!user;

  const value = {
    user,
    loading,
    login,
    register,
    logout,
    isAuthenticated,
    handleTokenExpiration,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
```

## 2. Middleware Implementation

The middleware now properly reads tokens from cookies and handles protected route redirects:

```typescript
// frontend/src/middleware.ts
import { NextRequest, NextResponse } from 'next/server';

// Define protected routes
const protectedRoutes = ['/dashboard', '/tasks'];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Allow auth pages and public routes
  if (pathname.startsWith('/(auth)') || pathname === '/' || pathname.startsWith('/api/')) {
    return NextResponse.next();
  }

  const isProtectedRoute = protectedRoutes.some(route =>
    pathname.startsWith(route)
  );

  // Read token from cookies
  const token = request.cookies.get('access_token')?.value;

  // If trying to access a protected route without authentication
  if (isProtectedRoute && !token) {
    const url = request.nextUrl.clone();
    url.pathname = '/(auth)/sign-in';
    return NextResponse.redirect(url);
  }

  // If user is authenticated and trying to access auth pages, redirect to dashboard
  if (token && pathname.startsWith('/(auth)')) {
    const url = request.nextUrl.clone();
    url.pathname = '/dashboard';
    return NextResponse.redirect(url);
  }

  return NextResponse.next();
}

// Specify which paths the middleware should run on
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};
```

## 3. Authentication Checks in Dashboard and Tasks Pages

Both dashboard and tasks pages now use the useAuth hook for authentication checks:

```typescript
// Example in dashboard page
'use client';

import React from 'react';
import { useTheme } from 'next-themes';
import { useAuth } from '@/providers/AuthProvider';
import ProtectedRoute from '@/components/ProtectedRoute';

const DashboardPage = () => {
  const { theme } = useTheme();
  const { user, loading } = useAuth();

  // ... rest of the component

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      </div>
    );
  }

  return (
    <ProtectedRoute>
      {/* Dashboard content */}
    </ProtectedRoute>
  );
};
```

## 4. Testing the Authentication Flow

### After Signing In:
1. Check browser console → network → token/cookie presence
2. Verify /dashboard opens
3. Verify /dashboard/tasks opens

### How to Test:
1. Start your backend server (FastAPI)
2. Start your frontend server (Next.js)
3. Navigate to http://localhost:3000/(auth)/sign-in
4. Sign in with valid credentials
5. Check that you're redirected to /dashboard
6. Verify that the token is stored in cookies (check Application tab in DevTools)
7. Navigate to /dashboard/tasks and verify access
8. Try navigating to /dashboard when not logged in - should redirect to sign-in

### Debugging Steps:
1. Check browser console for any errors
2. Check Network tab to see if API calls include Authorization header
3. Check Application tab to see if cookies are set properly
4. Verify router.push is working correctly
5. Check useEffect timing in components

## 5. Token Management Utilities

The token management utilities now use cookies for better security:

```typescript
// frontend/src/lib/auth/tokenUtils.ts
import Cookies from 'js-cookie';

// Function to get the JWT token from cookies
export const getToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return Cookies.get('access_token') || localStorage.getItem('jwt_token');
  }
  return null;
};

// Function to store the JWT token in cookies (with security options)
export const setToken = (token: string): void => {
  if (typeof window !== 'undefined') {
    // Store in cookie with security options
    Cookies.set('access_token', token, {
      expires: 7, // 7 days
      secure: process.env.NODE_ENV === 'production', // Only send over HTTPS in production
      sameSite: 'strict', // Prevent CSRF
      httpOnly: false, // Need to access via JS for API requests
    });

    // Also store in localStorage for backward compatibility
    localStorage.setItem('jwt_token', token);
  }
};

// Function to remove the JWT token from cookies and localStorage
export const removeToken = (): void => {
  if (typeof window !== 'undefined') {
    Cookies.remove('access_token');
    localStorage.removeItem('jwt_token');
  }
};

// Function to check if user is authenticated
export const isAuthenticated = (): boolean => {
  const token = getToken();
  if (!token) {
    return false;
  }

  // Check if token is expired
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const currentTime = Math.floor(Date.now() / 1000);
    return payload.exp > currentTime;
  } catch (error) {
    return false;
  }
};

// Function to get user info using the stored token
export const getUser = async (): Promise<any> => {
  const token = getToken();

  if (!token) {
    throw new Error('No token found');
  }

  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}/auth/me`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      if (response.status === 401) {
        // Token might be expired, remove it
        removeToken();
        throw new Error('Token is invalid or expired');
      }
      throw new Error(`Failed to fetch user data: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Get user error:', error);
    throw error;
  }
};
```

## 6. Protected Route Component

The ProtectedRoute component ensures only authenticated users can access certain pages:

```typescript
// frontend/src/components/ProtectedRoute.tsx
'use client';

import React, { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/providers/AuthProvider';

interface ProtectedRouteProps {
  children: React.ReactNode;
  redirectTo?: string;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  children,
  redirectTo = '/(auth)/sign-in'
}) => {
  const { isAuthenticated, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.replace(redirectTo);
    }
  }, [isAuthenticated, loading, router, redirectTo]);

  // Show loading spinner while checking authentication status
  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      </div>
    );
  }

  // If authenticated, render the protected content
  if (isAuthenticated) {
    return <>{children}</>;
  }

  // If not authenticated, return null (the redirect happens in useEffect)
  // This prevents rendering anything when redirecting
  return null;
};

export default ProtectedRoute;
```

## 7. Next.js Path Structure

The app router structure follows this pattern:
- `(auth)/sign-in` - Login page
- `(auth)/sign-up` - Registration page
- `dashboard` - Main dashboard
- `dashboard/tasks` - Tasks page
- `tasks` - Alternative tasks page
- `tasks/[id]` - Individual task page
- `tasks/new` - Create new task page

## 8. Common Issues and Solutions

### Issue: "Failed to fetch user data" error
Solution: The AuthProvider now checks for token existence before attempting to fetch user data. If the token is invalid or expired, it removes the token and sets the user to null.

### Issue: "[object Object],[object Object]" error during sign-in
Solution: The signIn function in tokenUtils now properly handles error responses from the backend. The LoginForm component also properly handles different error response formats to display meaningful error messages to the user. Additionally, the AuthProvider's login function now properly processes error responses before throwing them to the LoginForm.

### Issue: Redirects not working
Solution: Make sure AuthProvider wraps the entire app in layout.tsx

### Issue: Token not persisting
Solution: Check that cookies are enabled in the browser and that the domain settings are correct

### Issue: Protected routes accessible without authentication
Solution: Verify that the middleware is properly configured and that ProtectedRoute components are used in pages

### Issue: API calls not including Authorization header
Solution: Check that the axios interceptors are properly configured in the API service
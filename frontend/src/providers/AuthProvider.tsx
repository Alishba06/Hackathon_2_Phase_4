'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

import {
  getUser,
  signIn as signInUtil,
  signOut as signOutUtil,
  register as registerUser,
  removeToken,
  getToken,
  isAuthenticated as checkIsAuthenticated,
} from '@/lib/auth/tokenUtils';

interface AuthContextType {
  user: any | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (
    email: string,
    password: string,
    firstName?: string,
    lastName?: string
  ) => Promise<void>;
  logout: () => Promise<void>;
  isAuthenticated: boolean;
  handleTokenExpiration: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);

  const router = useRouter();

  // 🔐 CHECK AUTH ON APP LOAD
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const token = getToken();

        if (!token || !checkIsAuthenticated()) {
          setUser(null);
          return;
        }

        const userData = await getUser();
        setUser(userData);
      } catch (error) {
        console.error('Auth check failed:', error);
        removeToken();
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  // ---------------- LOGIN ----------------
  const login = async (email: string, password: string) => {
    try {
      setLoading(true);

      await signInUtil(email, password);

      const userData = await getUser();
      if (!userData) {
        throw new Error('Failed to fetch user after login');
      }

      setUser(userData);
      setLoading(false);

      // 🔥 IMPORTANT: replace, NOT push
      router.replace('/dashboard');
    } catch (error) {
      setLoading(false);
      console.error('Login failed:', error);
      throw error;
    }
  };

  // ---------------- REGISTER ----------------
  const register = async (
    email: string,
    password: string,
    firstName?: string,
    lastName?: string
  ) => {
    try {
      setLoading(true);

      await registerUser(email, password, firstName, lastName);

      const userData = await getUser();
      if (!userData) {
        throw new Error('Failed to fetch user after register');
      }

      setUser(userData);
      setLoading(false);

      router.replace('/dashboard');
    } catch (error) {
      setLoading(false);
      console.error('Registration failed:', error);
      throw error;
    }
  };

  // ---------------- LOGOUT ----------------
  const logout = async () => {
    try {
      await signOutUtil();
    } catch (error) {
      console.error('Logout failed:', error);
    } finally {
      removeToken();
      setUser(null);
      router.replace('/sign-in');
    }
  };

  // ---------------- TOKEN EXPIRE ----------------
  const handleTokenExpiration = () => {
    removeToken();
    setUser(null);
    router.replace('/sign-in');
  };

  // ✅ AUTH DECISION ONLY BASED ON TOKEN
  const isAuthenticated = !loading && checkIsAuthenticated();

  const value: AuthContextType = {
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
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};






// 'use client';

// import React, { createContext, useContext, useEffect, useState } from 'react';
// import { useRouter } from 'next/navigation';
// import { getUser, signIn as signInUtil, signOut as signOutUtil, register as registerUser, removeToken, getToken, isAuthenticated as checkIsAuthenticated } from '@/lib/auth/tokenUtils';

// // Define the shape of our auth context
// interface AuthContextType {
//   user: any | null;
//   loading: boolean;
//   login: (email: string, password: string) => Promise<void>;
//   register: (email: string, password: string, firstName?: string, lastName?: string) => Promise<void>;
//   logout: () => Promise<void>;
//   isAuthenticated: boolean;
//   handleTokenExpiration: () => void;
// }

// // Create the auth context
// const AuthContext = createContext<AuthContextType | undefined>(undefined);

// export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
//   const [user, setUser] = useState<any | null>(null);
//   const [loading, setLoading] = useState(true);
//   const router = useRouter();

//   // Check if user is authenticated on mount
//   useEffect(() => {
//     const checkAuth = async () => {
//       try {
//         // First check if we have a token and if it's valid
//         const token = getToken();
//         if (!token || !checkIsAuthenticated()) {
//           // No token or token is invalid/expired
//           setUser(null);
//           setLoading(false);
//           return;
//         }

//         // Token exists and appears valid, try to get user data
//         const userData = await getUser();
//         setUser(userData);
//       } catch (error: any) {
//         console.error('Auth check failed:', error);

//         // If auth check fails, remove the invalid token and set user to null
//         removeToken();
//         setUser(null);
//       } finally {
//         setLoading(false);
//       }
//     };

//     checkAuth();
//   }, []);

//   // ------------------- LOGIN -------------------
//   const login = async (email: string, password: string) => {
//     try {
//       // Sign in and get token
//       await signInUtil(email, password);

//       // Fetch user profile using token
//       const userData = await getUser();
//       if (!userData) {
//         throw new Error('Failed to fetch user profile after login.');
//       }

//       setUser(userData);

//       // Wait for state update before redirecting to ensure user is set
//       setTimeout(() => {
//         router.push('/dashboard');
//       }, 0);
//     } catch (error: any) {
//       console.error('Login failed:', error);

//       // Properly handle different error types
//       let errorMessage = 'Login failed. Please try again.';

//       if (error instanceof Error) {
//         errorMessage = error.message;
//       } else if (typeof error === 'string') {
//         errorMessage = error;
//       } else if (error && typeof error === 'object' && error.detail) {
//         errorMessage = error.detail;
//       } else if (error && typeof error === 'object' && error.message) {
//         errorMessage = error.message;
//       }

//       // Throw the processed error message
//       throw new Error(errorMessage);
//     }
//   };

//   // ------------------- REGISTER -------------------
//   const register = async (email: string, password: string, firstName?: string, lastName?: string) => {
//     try {
//       // Register user and get token
//       await registerUser(email, password, firstName, lastName);

//       // Fetch user profile using token
//       const userData = await getUser();
//       if (!userData) {
//         throw new Error('Failed to fetch user profile after registration.');
//       }

//       setUser(userData);

//       // Wait for state update before redirecting to ensure user is set
//       setTimeout(() => {
//         router.push('/dashboard');
//       }, 0);
//     } catch (error: any) {
//       console.error('Registration failed:', error);

//       if (error.message?.includes('Network Error')) {
//         alert('Could not connect to the server. Please make sure the backend is running.');
//       }

//       throw error;
//     }
//   };

//   // ------------------- LOGOUT -------------------
//   const logout = async () => {
//     try {
//       await signOutUtil();
//     } catch (error) {
//       console.error('Logout failed:', error);
//       // Even if the backend logout fails, clear local token and user data
//       removeToken();
//     } finally {
//       setUser(null);
//       router.push('/(auth)/sign-in'); // redirect to login
//     }
//   };

//   // ------------------- HANDLE TOKEN EXPIRATION -------------------
//   const handleTokenExpiration = () => {
//     setUser(null);
//     removeToken(); // Use the new utility function
//     router.push('/(auth)/sign-in');
//   };

//   // Calculate isAuthenticated based on token validity, not just user state
//   // This prevents redirect loops when user state is temporarily null during updates
//   const isAuthenticated = !loading && user !== null && user !== undefined;

//   const value = {
//     user,
//     loading,
//     login,
//     register,
//     logout,
//     isAuthenticated,
//     handleTokenExpiration,
//   };

//   return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
// };

// export const useAuth = () => {
//   const context = useContext(AuthContext);
//   if (!context) {
//     throw new Error('useAuth must be used within an AuthProvider');
//   }
//   return context;
// };












// 'use client';

// import React, { createContext, useContext, useEffect, useState } from 'react';
// import { useRouter } from 'next/navigation';
// import { getUser, signIn, signOut, register as registerUser } from '@/lib/auth/tokenUtils';

// // Define the shape of our auth context
// interface AuthContextType {
//   user: any | null;
//   loading: boolean;
//   login: (email: string, password: string) => Promise<void>;
//   register: (email: string, password: string, firstName?: string, lastName?: string) => Promise<void>;
//   logout: () => Promise<void>;
//   isAuthenticated: boolean;
//   handleTokenExpiration: () => void;
// }

// // Create the auth context
// const AuthContext = createContext<AuthContextType | undefined>(undefined);

// export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
//   const [user, setUser] = useState<any | null>(null);
//   const [loading, setLoading] = useState(true);
//   const router = useRouter();

//   // Check if user is authenticated on mount
//   useEffect(() => {
//     const checkAuth = async () => {
//       try {
//         const userData = await getUser();
//         setUser(userData);
//       } catch (error) {
//         console.error('Auth check failed:', error);
//         setUser(null);
//       } finally {
//         setLoading(false);
//       }
//     };

//     checkAuth();
//   }, []);

//   const login = async (email: string, password: string) => {
//     try {
//       const response = await signIn(email, password);
//       // Ensure we have user data in the response
//       if (response.user) {
//         setUser(response.user);
//       } else {
//         // If user data is not in the response, fetch it separately
//         const userData = await getUser();
//         setUser(userData);
//       }
//       // Wait for state update before redirecting
//       setTimeout(() => {
//         router.push('/dashboard');
//       }, 0);
//     } catch (error: any) {
//       console.error('Login failed:', error);

//       // Check if it's a network error
//       if (error.code === 'ERR_NETWORK') {
//         alert('Could not connect to the server. Please make sure the backend is running.');
//       }

//       throw error;
//     }
//   };

//   const register = async (email: string, password: string, firstName?: string, lastName?: string) => {
//     try {
//       // Call the registration API
//       const response = await registerUser(email, password, firstName, lastName);
//       // Ensure we have user data in the response
//       if (response.user) {
//         setUser(response.user);
//       } else {
//         // If user data is not in the response, fetch it separately
//         const userData = await getUser();
//         setUser(userData);
//       }
//       // Wait for state update before redirecting
//       setTimeout(() => {
//         router.push('/dashboard');
//       }, 0);
//     } catch (error: any) {
//       console.error('Registration failed:', error);

//       // Check if it's a network error
//       if (error.code === 'ERR_NETWORK') {
//         alert('Could not connect to the server. Please make sure the backend is running.');
//       }

//       throw error;
//     }
//   };

//   const logout = async () => {
//     try {
//       await signOut();
//       setUser(null);
//       router.push('/(auth)/sign-in');
//     } catch (error) {
//       console.error('Logout failed:', error);
//       // Even if logout fails, redirect to login
//       setUser(null);
//       router.push('/(auth)/sign-in');
//     }
//   };

//   const handleTokenExpiration = () => {
//     // Clear user data and redirect to login
//     setUser(null);
//     localStorage.removeItem('jwt_token');
//     router.push('/(auth)/sign-in');
//   };

//   const isAuthenticated = !!user;

//   const value = {
//     user,
//     loading,
//     login,
//     register,
//     logout,
//     isAuthenticated,
//     handleTokenExpiration
//   };

//   return (
//     <AuthContext.Provider value={value}>
//       {children}
//     </AuthContext.Provider>
//   );
// };

// export const useAuth = () => {
//   const context = useContext(AuthContext);
//   if (context === undefined) {
//     throw new Error('useAuth must be used within an AuthProvider');
//   }
//   return context;
// };
'use client';

import React, { useEffect, useState } from 'react';
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
  const [checkedAuth, setCheckedAuth] = useState(false);

  // Effect to handle redirect when user is not authenticated
  useEffect(() => {
    if (!loading) {
      if (!isAuthenticated) {
        router.replace(redirectTo);
      } else {
        setCheckedAuth(true);
      }
    } else {
      // If still loading, don't render anything yet
      setCheckedAuth(false);
    }
  }, [isAuthenticated, loading, router, redirectTo]);

  // Show loading spinner while checking authentication status
  if (loading || !checkedAuth) {
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

  // If not authenticated, the redirect should have happened by now
  return null;
};

export default ProtectedRoute;
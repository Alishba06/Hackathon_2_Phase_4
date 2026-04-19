import { NextRequest, NextResponse } from 'next/server';

// Define protected routes - be more specific to avoid conflicts with nested routes
const protectedRoutes = [
  '/dashboard',
  '/tasks',
  // Add more specific routes if needed, but avoid conflicts with nested routes
];

export function middleware(request: NextRequest) {
  // Check if the requested path is an exact match or starts with a protected route
  // But exclude nested routes that might be public
  const isProtectedRoute = protectedRoutes.some(route =>
    request.nextUrl.pathname === route ||
    request.nextUrl.pathname.startsWith(route + '/') // Ensures /dashboard/xyz but not /dashboardxyz
  );

  // Check if the requested path is an auth route
  const isAuthRoute = request.nextUrl.pathname === '/sign-in' ||
                     request.nextUrl.pathname === '/sign-up' ||
                     request.nextUrl.pathname === '/(auth)/sign-in' ||
                     request.nextUrl.pathname === '/(auth)/sign-up';

  // Get the token from cookies or headers (since localStorage isn't available in middleware)
  // Look for both possible cookie names that the token might be stored under
  const accessToken = request.cookies.get('access_token')?.value;
  const jwtToken = request.cookies.get('jwt_token')?.value;
  const token = accessToken || jwtToken ||
                request.headers.get('authorization')?.replace('Bearer ', '') ||
                request.headers.get('x-auth-token');

  // Check if user has a valid token
  const isAuthenticated = !!token;

  // If trying to access a protected route without authentication
  if (isProtectedRoute && !isAuthenticated) {
    // Redirect to login page - use the correct path (without the route group parentheses)
    return NextResponse.redirect(new URL('/sign-in', request.url));
  }

  // If user is authenticated and trying to access auth pages, redirect to dashboard
  if (isAuthenticated && isAuthRoute) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  // Allow the request to proceed
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
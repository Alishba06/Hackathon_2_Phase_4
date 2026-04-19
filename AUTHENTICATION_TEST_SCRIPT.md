# Authentication Flow Test Script

This script outlines the steps to test the authentication and routing functionality of your Next.js + FastAPI Todo App.

## Prerequisites
1. Backend server (FastAPI) running on http://localhost:8000
2. Frontend server (Next.js) running on http://localhost:3000

## Test Steps

### 1. Verify Initial State
1. Open browser and navigate to http://localhost:3000
2. Verify that you can access the home page without authentication
3. Try to navigate directly to http://localhost:3000/dashboard
4. Verify that you are redirected to http://localhost:3000/(auth)/sign-in

### 2. Test Sign-In Flow
1. Navigate to http://localhost:3000/(auth)/sign-in
2. Enter valid credentials (or create an account if needed)
3. Submit the form
4. Verify that you are redirected to http://localhost:3000/dashboard
5. Check browser console for any errors
6. Check Application tab in DevTools:
   - Look for 'access_token' in Cookies
   - Look for 'jwt_token' in Local Storage

### 3. Test Dashboard Access
1. After successful sign-in, verify that the dashboard page loads
2. Check that user information is displayed correctly
3. Verify that the loading indicator disappears
4. Check that the theme is applied correctly

### 4. Test Tasks Page Access
1. Navigate to http://localhost:3000/dashboard/tasks
2. Verify that the page loads without redirecting to sign-in
3. Check that tasks are loaded (if any exist)
4. Verify that you can interact with the tasks (toggle, delete, etc.)

### 5. Test Protected Routes
1. Log out from the application
2. Try to navigate directly to http://localhost:3000/dashboard
3. Verify that you are redirected to http://localhost:3000/(auth)/sign-in
4. Repeat for http://localhost:3000/dashboard/tasks

### 6. Test Sign-Up Flow
1. Navigate to http://localhost:3000/(auth)/sign-up
2. Enter valid registration details
3. Submit the form
4. Verify that you are redirected to http://localhost:3000/dashboard
5. Check that the new user account is created in the database

### 7. Test Logout Flow
1. While logged in, trigger the logout function
2. Verify that you are redirected to http://localhost:3000/(auth)/sign-in
3. Check that the 'access_token' cookie is removed
4. Check that the 'jwt_token' local storage is removed
5. Try to navigate to http://localhost:3000/dashboard - should redirect to sign-in

### 8. Test Token Expiration
1. Manually expire the token (by changing the expiration time in the JWT)
2. Try to access a protected route
3. Verify that you are redirected to the sign-in page
4. Check that the token is removed from storage

### 9. Test Network Requests
1. Open Network tab in DevTools
2. Perform actions that make API requests (fetching tasks, creating tasks, etc.)
3. Verify that each request includes the Authorization header with the Bearer token
4. Check that responses are handled correctly

### 10. Test Edge Cases
1. Try to access protected routes with an invalid/expired token
2. Verify that the application handles the 401 response correctly
3. Test signing in with invalid credentials
4. Verify that appropriate error messages are displayed

## Expected Behaviors

### Successful Authentication
- User credentials are validated against the backend
- JWT token is received and stored securely
- User is redirected to the dashboard
- User information is available in the application state

### Failed Authentication
- Appropriate error messages are displayed
- User remains on the sign-in page
- No token is stored

### Protected Route Access
- Unauthenticated users are redirected to sign-in
- Authenticated users can access protected routes
- Loading states are properly handled

### Token Management
- Tokens are stored securely (cookies + localStorage)
- Tokens are removed on logout
- Expired tokens trigger re-authentication

## Troubleshooting

### If redirects are not working:
- Check that AuthProvider is wrapping the entire app in layout.tsx
- Verify that middleware is properly configured
- Check that ProtectedRoute components are used in pages

### If tokens are not persisting:
- Check browser settings to ensure cookies are enabled
- Verify that the domain settings are correct
- Check for any browser extensions that might block cookies

### If API calls are failing:
- Verify that the backend server is running
- Check that the API base URL is correctly configured
- Ensure that the Authorization header is included in requests

### If protected routes are accessible without authentication:
- Verify that the middleware is properly configured
- Check that ProtectedRoute components are used in pages
- Ensure that the token validation logic is working correctly
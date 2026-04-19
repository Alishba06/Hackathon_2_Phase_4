# Quickstart Guide: Frontend Application & Authentication Integration

## Overview
This guide provides instructions for setting up and running the frontend application with Better Auth integration for the Todo web application.

## Prerequisites
- Node.js 18.x or higher
- npm or yarn package manager
- Access to the backend API (FastAPI server running)
- Valid JWT secret for Better Auth (shared with backend)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Navigate to Frontend Directory
```bash
cd frontend
```

### 3. Install Dependencies
```bash
npm install
# or
yarn install
```

### 4. Environment Configuration
Create a `.env.local` file in the frontend directory with the following variables:

```env
NEXT_PUBLIC_API_BASE_URL=<backend_api_url>
NEXT_PUBLIC_BETTER_AUTH_URL=<better_auth_url>
NEXT_PUBLIC_JWT_SECRET=<jwt_secret_shared_with_backend>
```

### 5. Run the Development Server
```bash
npm run dev
# or
yarn dev
```

The application will be available at `http://localhost:3000`.

## Key Features Setup

### Better Auth Integration
1. The application is configured to use Better Auth for user authentication
2. JWT tokens are automatically handled by the auth client
3. Authentication state is managed through React Context

### API Client Configuration
1. The API client is configured to automatically attach JWT tokens to requests
2. All authenticated requests will include the `Authorization: Bearer <token>` header
3. Error handling is implemented for common API responses

### Responsive Design
1. The UI is built with Tailwind CSS for responsive design
2. Components adapt to different screen sizes (mobile, tablet, desktop)
3. Touch-friendly interfaces for mobile devices

## Running Tests
```bash
# Run unit tests
npm run test
# or
yarn test

# Run end-to-end tests
npm run test:e2e
# or
yarn test:e2e
```

## Building for Production
```bash
npm run build
# or
yarn build
```

## Deployment
The application is configured for deployment to platforms like Vercel, Netlify, or any hosting service that supports Next.js applications.

### Environment Variables for Production
Ensure the following environment variables are set in your production environment:
- `NEXT_PUBLIC_API_BASE_URL`: Production backend API URL
- `NEXT_PUBLIC_BETTER_AUTH_URL`: Production Better Auth URL
- `NEXT_PUBLIC_JWT_SECRET`: JWT secret for token validation

## Troubleshooting

### Common Issues
1. **JWT Token Not Attached**: Ensure the user is properly authenticated and the token is stored in the session
2. **Authentication Failing**: Verify that the JWT secret matches between frontend and backend
3. **API Requests Failing**: Check that the backend API is running and accessible from the frontend

### Debugging Tips
1. Check browser developer tools for API request/response details
2. Verify that environment variables are correctly set
3. Ensure the backend API is running and accessible
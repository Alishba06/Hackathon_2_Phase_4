# Todo Frontend Application

This is the frontend for the Todo web application built with Next.js 16+ and integrated with Better Auth for authentication.

## Features

- User authentication (sign up, sign in, sign out)
- JWT token handling for secure API communication
- Task management (create, read, update, delete)
- Responsive design for mobile, tablet, and desktop
- Protected routes and authentication middleware

## Tech Stack

- Next.js 16+ with App Router
- React 19+
- TypeScript
- Tailwind CSS for styling
- Better Auth for authentication
- Axios for API requests

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create a `.env.local` file in the root of the frontend directory with the following variables:
```env
NEXT_PUBLIC_API_BASE_URL=<backend_api_url>
NEXT_PUBLIC_BETTER_AUTH_URL=<better_auth_url>
NEXT_PUBLIC_JWT_SECRET=<jwt_secret_shared_with_backend>
```

3. Run the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`.

## Scripts

- `npm run dev` - Start the development server
- `npm run build` - Build the application for production
- `npm run start` - Start the production server
- `npm run lint` - Run ESLint
- `npm run test` - Run tests

## Project Structure

```
frontend/
├── src/
│   ├── app/                 # Next.js App Router pages
│   │   ├── (auth)/          # Authentication-related pages
│   │   │   ├── sign-in/
│   │   │   └── sign-up/
│   │   ├── dashboard/       # Main dashboard with task management
│   │   ├── tasks/           # Task-related pages
│   │   │   ├── [id]/        # Individual task pages
│   │   │   └── new/         # Create new task page
│   │   ├── layout.tsx       # Root layout
│   │   └── page.tsx         # Home page
│   ├── components/          # Reusable UI components
│   │   ├── auth/            # Authentication components
│   │   ├── tasks/           # Task management components
│   │   ├── ui/              # Base UI components (buttons, inputs, etc.)
│   │   └── providers/       # Context providers (AuthProvider, etc.)
│   ├── lib/                 # Utility functions and constants
│   │   ├── auth/            # Authentication utilities
│   │   ├── api/             # API client and request functions
│   │   └── utils/           # General utility functions
│   ├── hooks/               # Custom React hooks
│   │   └── useAuth.ts       # Authentication hook
│   └── styles/              # Global styles and Tailwind config
├── public/                  # Static assets
├── package.json             # Dependencies and scripts
├── tailwind.config.js       # Tailwind CSS configuration
├── next.config.js           # Next.js configuration
└── tsconfig.json            # TypeScript configuration
```

## API Integration

The frontend communicates with the backend API using the centralized API client located at `src/lib/api/client.ts`. All authenticated requests automatically include the JWT token in the Authorization header.

## Authentication Flow

1. User registers or signs in via the authentication pages
2. JWT token is received and stored in localStorage
3. The token is automatically attached to all API requests
4. Middleware protects routes that require authentication
5. Tokens are validated on each request, and users are redirected if invalid/expired
'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/providers/AuthProvider';
import { Button } from '../ui/Button';
import Input from '../ui/Input';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle
} from '../ui/Card';

const LoginForm: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const router = useRouter();
  const { login } = useAuth(); // login from AuthProvider

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Call login function from AuthProvider
      // The AuthProvider handles token storage and redirection
      await login(email, password);
      console.log('Login success');
    } catch (err: any) {
      console.error('Login failed:', err);

      // Proper error handling
      let errorMessage = 'Login failed. Please check your credentials.';

      if (err instanceof Error) {
        errorMessage = err.message;
      } else if (typeof err === 'string') {
        errorMessage = err;
      } else if (err && typeof err === 'object') {
        if (err.detail) errorMessage = err.detail;
        else if (err.message) errorMessage = err.message;
        else if (err.error) errorMessage = err.error;
        else {
          try {
            errorMessage = JSON.stringify(err);
          } catch {
            errorMessage = 'An unknown error occurred during login.';
          }
        }
      }

      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader className="space-y-1">
        <CardTitle className="text-2xl">Sign in</CardTitle>
        <CardDescription>
          Enter your credentials to access your account
        </CardDescription>
      </CardHeader>

      <form onSubmit={handleSubmit}>
        <CardContent className="space-y-4">
          {error && (
            <div className="p-3 bg-red-100 text-red-700 rounded-md text-sm">
              {error}
            </div>
          )}

          <Input
            label="Email"
            type="email"
            placeholder="name@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <Input
            label="Password"
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </CardContent>

        <CardFooter className="flex flex-col">
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? 'Signing in...' : 'Sign In'}
          </Button>

          <div className="mt-4 text-center text-sm">
            Don&apos;t have an account?{' '}
            <a href="/(auth)/sign-up" className="underline">
              Sign up
            </a>
          </div>
        </CardFooter>
      </form>
    </Card>
  );
};

export default LoginForm;









// 'use client';

// import React, { useState } from 'react';
// import { useRouter } from 'next/navigation';
// import { useAuth } from '@/providers/AuthProvider';
// import { Button } from '../ui/Button'; // ✅ FIX
// import Input from '../ui/Input';
// import {
//   Card,
//   CardContent,
//   CardDescription,
//   CardFooter,
//   CardHeader,
//   CardTitle
// } from '../ui/Card';

// const LoginForm: React.FC = () => {
//   const [email, setEmail] = useState('');
//   const [password, setPassword] = useState('');
//   const [error, setError] = useState('');
//   const [loading, setLoading] = useState(false);

//   const router = useRouter();
//   const { login } = useAuth();

//   const handleSubmit = async (e: React.FormEvent) => {
//     e.preventDefault();
//     setError('');
//     setLoading(true);

//     try {
//       await login(email, password);
//       // The redirect is now handled in the AuthProvider after state update
//     } catch (err: any) {
//       // Handle error properly - err could be a string or object
//       let errorMessage = 'Login failed. Please check your credentials.';

//       if (err instanceof Error) {
//         errorMessage = err.message;
//       } else if (typeof err === 'string') {
//         errorMessage = err;
//       } else if (err && typeof err === 'object') {
//         // Handle object errors
//         if (err.detail) {
//           errorMessage = err.detail;
//         } else if (err.message) {
//           errorMessage = err.message;
//         } else if (err.error) {
//           errorMessage = err.error;
//         } else {
//           // If it's a generic object, try to stringify it
//           try {
//             errorMessage = JSON.stringify(err);
//           } catch (stringifyErr) {
//             errorMessage = 'An unknown error occurred during login.';
//           }
//         }
//       }

//       setError(errorMessage);
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <Card className="w-full max-w-md mx-auto">
//       <CardHeader className="space-y-1">
//         <CardTitle className="text-2xl">Sign in</CardTitle>
//         <CardDescription>
//           Enter your credentials to access your account
//         </CardDescription>
//       </CardHeader>

//       <form onSubmit={handleSubmit}>
//         <CardContent className="space-y-4">
//           {error && (
//             <div className="p-3 bg-red-100 text-red-700 rounded-md text-sm">
//               {error}
//             </div>
//           )}

//           <Input
//             label="Email"
//             type="email"
//             placeholder="name@example.com"
//             value={email}
//             onChange={(e) => setEmail(e.target.value)}
//             required
//           />

//           <Input
//             label="Password"
//             type="password"
//             placeholder="Enter your password"
//             value={password}
//             onChange={(e) => setPassword(e.target.value)}
//             required
//           />
//         </CardContent>

//         <CardFooter className="flex flex-col">
//           <Button
//             type="submit"
//             className="w-full"
//             disabled={loading}
//           >
//             {loading ? 'Signing in...' : 'Sign In'}
//           </Button>

//           <div className="mt-4 text-center text-sm">
//             Don&apos;t have an account?{' '}
//             <a href="/(auth)/sign-up" className="underline">
//               Sign up
//             </a>
//           </div>
//         </CardFooter>
//       </form>
//     </Card>
//   );
// };

// export default LoginForm;

















// 'use client';

// import React, { useState } from 'react';
// import { useRouter } from 'next/navigation';
// import { useAuth } from '@/providers/AuthProvider';
// import Button from '../ui/Button';
// import Input from '../ui/Input';
// import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '../ui/Card';

// const LoginForm: React.FC = () => {
//   const [email, setEmail] = useState('');
//   const [password, setPassword] = useState('');
//   const [error, setError] = useState('');
//   const [loading, setLoading] = useState(false);

//   const router = useRouter();
//   const { login } = useAuth();

//   const handleSubmit = async (e: React.FormEvent) => {
//     e.preventDefault();
//     setError('');
//     setLoading(true);

//     try {
//       await login(email, password);
//       router.push('/dashboard');
//     } catch (err: any) {
//       setError(err.response?.data?.message || 'Login failed. Please check your credentials.');
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <Card className="w-full max-w-md mx-auto">
//       <CardHeader className="space-y-1">
//         <CardTitle className="text-2xl">Sign in</CardTitle>
//         <CardDescription>
//           Enter your credentials to access your account
//         </CardDescription>
//       </CardHeader>
//       <form onSubmit={handleSubmit}>
//         <CardContent className="space-y-4">
//           {error && (
//             <div className="p-3 bg-red-100 text-red-700 rounded-md text-sm">
//               {error}
//             </div>
//           )}
//           <Input
//             label="Email"
//             type="email"
//             placeholder="name@example.com"
//             value={email}
//             onChange={(e) => setEmail(e.target.value)}
//             required
//           />
//           <Input
//             label="Password"
//             type="password"
//             placeholder="Enter your password"
//             value={password}
//             onChange={(e) => setPassword(e.target.value)}
//             required
//           />
//         </CardContent>
//         <CardFooter className="flex flex-col">
//           <Button
//             type="submit"
//             className="w-full"
//             isLoading={loading}
//             disabled={loading}
//           >
//             Sign In
//           </Button>
//           <div className="mt-4 text-center text-sm">
//             Don't have an account?{' '}
//             <a href="/(auth)/sign-up" className="underline">
//               Sign up
//             </a>
//           </div>
//         </CardFooter>
//       </form>
//     </Card>
//   );
// };

// export default LoginForm;
# Fixed Login Implementation

Here's the corrected implementation for your login form to avoid the "[object Object]" error:

## Updated Login Function

```typescript
interface LoginResponse {
  token: string;
  user: {
    id: string;
    email: string;
    firstName?: string;
    lastName?: string;
  };
  // Add other fields as needed based on your API response
}

async function login(email: string, password: string): Promise<LoginResponse> {
  try {
    const response = await axios.post('/api/login', { email, password });
    
    // Return only the data portion of the response, not the full Axios response object
    return response.data;
  } catch (error: any) {
    // Handle different types of errors appropriately
    if (error.response) {
      // Server responded with error status
      throw new Error(error.response.data.message || 'Login failed');
    } else if (error.request) {
      // Request was made but no response received
      throw new Error('Network error: Unable to reach server');
    } else {
      // Something else happened
      throw new Error(error.message || 'An unexpected error occurred');
    }
  }
}
```

## Updated handleSubmit Function

```typescript
const [error, setError] = useState<string | null>(null);
const [loading, setLoading] = useState<boolean>(false);

const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  setError(null);
  setLoading(true);

  try {
    const loginData = await login(email, password);
    
    // Now you can properly access the token and user data
    const { token, user } = loginData;
    
    // Store the token (in localStorage, cookie, or context/state)
    localStorage.setItem('authToken', token);
    
    // Update your app state with user data
    // For example, if using a context:
    // setCurrentUser(user);
    
    console.log('Login successful!', user.email);
    
    // Redirect user or update UI as needed
    // router.push('/dashboard');
    
  } catch (err: any) {
    // Properly handle and display error messages
    const errorMessage = err.message || 'Login failed. Please try again.';
    setError(errorMessage);
    console.error('Login error:', err);
  } finally {
    setLoading(false);
  }
};
```

## Complete Component Example

```typescript
import React, { useState } from 'react';
import axios from 'axios';

interface LoginResponse {
  token: string;
  user: {
    id: string;
    email: string;
    firstName?: string;
    lastName?: string;
  };
}

interface User {
  id: string;
  email: string;
  firstName?: string;
  lastName?: string;
}

const LoginForm: React.FC = () => {
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [currentUser, setCurrentUser] = useState<User | null>(null);

  async function login(email: string, password: string): Promise<LoginResponse> {
    try {
      const response = await axios.post('/api/login', { email, password });
      
      // Return only the data portion of the response
      return response.data;
    } catch (error: any) {
      if (error.response) {
        // Server responded with error status
        throw new Error(error.response.data.message || 'Login failed');
      } else if (error.request) {
        // Request was made but no response received
        throw new Error('Network error: Unable to reach server');
      } else {
        // Something else happened
        throw new Error(error.message || 'An unexpected error occurred');
      }
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const loginData = await login(email, password);
      
      // Destructure the response to get token and user data
      const { token, user } = loginData;
      
      // Store the token
      localStorage.setItem('authToken', token);
      
      // Update your app state with user data
      setCurrentUser(user);
      
      console.log('Login successful!', user.email);
      
      // Redirect user or update UI as needed
      // router.push('/dashboard');
      
    } catch (err: any) {
      // Properly handle and display error messages
      const errorMessage = err.message || 'Login failed. Please try again.';
      setError(errorMessage);
      console.error('Login error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="email">Email:</label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
      </div>
      
      <div>
        <label htmlFor="password">Password:</label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </div>
      
      {error && <div style={{ color: 'red' }}>{error}</div>}
      
      <button type="submit" disabled={loading}>
        {loading ? 'Logging in...' : 'Login'}
      </button>
    </form>
  );
};

export default LoginForm;
```

## Key Points:

1. **Return response.data**: Always return `response.data` instead of the full Axios response object
2. **Type Safety**: Define interfaces for your API responses to ensure type safety
3. **Error Handling**: Properly handle different types of errors (network, server, etc.)
4. **State Management**: Update your app state with the returned user data after successful login
5. **Token Storage**: Store the authentication token appropriately (localStorage, cookies, etc.)

This implementation will prevent the "[object Object]" error and allow you to properly access the token and user data returned from your login API.
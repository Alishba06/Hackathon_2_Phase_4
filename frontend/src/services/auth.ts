// frontend/src/services/auth.ts

// Export the token utilities from the new tokenUtils file
export {
  getToken,
  setToken,
  removeToken,
  isAuthenticated,
  getUserIdFromToken
} from '@/lib/auth/tokenUtils';
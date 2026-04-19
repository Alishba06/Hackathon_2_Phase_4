// AuthAgent - Secure Authentication & Authorization Agent
//
// Purpose: Handle user authentication and authorization flows securely across the application
// Responsibilities: Secure signup/signin flows, password hashing, JWT management,
// authentication guards, session management, Better Auth integration, OWASP compliance

class AuthAgent {
  constructor(options = {}) {
    this.config = {
      // Default configuration values
      passwordMinLength: options.passwordMinLength || 8,
      passwordRequireComplexity: options.passwordRequireComplexity || true,
      jwtSecret: options.jwtSecret || process.env.JWT_SECRET,
      refreshTokenExpiry: options.refreshTokenExpiry || '7d',
      accessTokenExpiry: options.accessTokenExpiry || '15m',
      sessionTimeout: options.sessionTimeout || 30 * 60 * 1000, // 30 minutes
      rateLimitWindow: options.rateLimitWindow || 15 * 60 * 1000, // 15 minutes
      maxLoginAttempts: options.maxLoginAttempts || 5,
      ...options
    };

    // Initialize security modules
    this.passwordHasher = this.initializePasswordHasher();
    this.tokenManager = this.initializeTokenManager();
    this.sessionManager = this.initializeSessionManager();
    this.rateLimiter = this.initializeRateLimiter();
  }

  initializePasswordHasher() {
    // Using bcrypt for password hashing
    const bcrypt = require('bcrypt');
    
    return {
      hash: async (password) => {
        const saltRounds = this.config.saltRounds || 12;
        return await bcrypt.hash(password, saltRounds);
      },
      compare: async (password, hash) => {
        return await bcrypt.compare(password, hash);
      }
    };
  }

  initializeTokenManager() {
    const jwt = require('jsonwebtoken');
    
    return {
      generateAccessToken: (payload) => {
        return jwt.sign(payload, this.config.jwtSecret, {
          expiresIn: this.config.accessTokenExpiry
        });
      },
      generateRefreshToken: (payload) => {
        return jwt.sign(payload, this.config.jwtSecret, {
          expiresIn: this.config.refreshTokenExpiry
        });
      },
      verifyToken: (token) => {
        try {
          return jwt.verify(token, this.config.jwtSecret);
        } catch (error) {
          throw new Error('Invalid token');
        }
      },
      refreshAccessToken: (refreshToken, newPayload) => {
        try {
          // Verify the refresh token
          const decoded = jwt.verify(refreshToken, this.config.jwtSecret);
          
          // Generate new access token
          return jwt.sign(newPayload, this.config.jwtSecret, {
            expiresIn: this.config.accessTokenExpiry
          });
        } catch (error) {
          throw new Error('Invalid refresh token');
        }
      }
    };
  }

  initializeSessionManager() {
    // Simple in-memory session store (should use Redis or DB in production)
    const sessions = new Map();
    
    return {
      createSession: (userId) => {
        const sessionId = this.generateSecureId();
        const sessionData = {
          userId,
          createdAt: Date.now(),
          lastAccessed: Date.now(),
          expiresAt: Date.now() + this.config.sessionTimeout
        };
        
        sessions.set(sessionId, sessionData);
        return sessionId;
      },
      
      getSession: (sessionId) => {
        const session = sessions.get(sessionId);
        if (!session) {
          return null;
        }
        
        // Check if session has expired
        if (Date.now() > session.expiresAt) {
          sessions.delete(sessionId);
          return null;
        }
        
        // Update last accessed time
        session.lastAccessed = Date.now();
        sessions.set(sessionId, session);
        return session;
      },
      
      destroySession: (sessionId) => {
        sessions.delete(sessionId);
      },
      
      extendSession: (sessionId) => {
        const session = sessions.get(sessionId);
        if (session) {
          session.expiresAt = Date.now() + this.config.sessionTimeout;
          sessions.set(sessionId, session);
        }
      }
    };
  }

  initializeRateLimiter() {
    const attempts = new Map();
    
    return {
      recordAttempt: (identifier) => {
        const now = Date.now();
        if (!attempts.has(identifier)) {
          attempts.set(identifier, []);
        }
        
        const userAttempts = attempts.get(identifier);
        userAttempts.push(now);
        
        // Clean up old attempts outside the window
        const windowStart = now - this.config.rateLimitWindow;
        const filteredAttempts = userAttempts.filter(time => time > windowStart);
        attempts.set(identifier, filteredAttempts);
        
        return filteredAttempts.length;
      },
      
      isBlocked: (identifier) => {
        const userAttempts = attempts.get(identifier) || [];
        const windowStart = Date.now() - this.config.rateLimitWindow;
        const recentAttempts = userAttempts.filter(time => time > windowStart);
        return recentAttempts.length >= this.config.maxLoginAttempts;
      }
    };
  }

  generateSecureId() {
    // Generate a cryptographically secure random ID
    const crypto = require('crypto');
    return crypto.randomBytes(32).toString('hex');
  }

  validatePassword(password) {
    if (password.length < this.config.passwordMinLength) {
      throw new Error(`Password must be at least ${this.config.passwordMinLength} characters long`);
    }

    if (this.config.passwordRequireComplexity) {
      // Check for at least one uppercase, lowercase, number, and special character
      const hasUpper = /[A-Z]/.test(password);
      const hasLower = /[a-z]/.test(password);
      const hasNumber = /\d/.test(password);
      const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);

      if (!(hasUpper && hasLower && hasNumber && hasSpecial)) {
        throw new Error('Password must contain at least one uppercase letter, lowercase letter, number, and special character');
      }
    }

    return true;
  }

  async signup(userData) {
    try {
      // Validate input
      if (!userData.email || !userData.password) {
        throw new Error('Email and password are required');
      }

      // Validate password strength
      this.validatePassword(userData.password);

      // Hash the password
      const hashedPassword = await this.passwordHasher.hash(userData.password);

      // Create user (this would typically involve saving to a database)
      const user = {
        id: this.generateSecureId(),
        email: userData.email.toLowerCase().trim(),
        password: hashedPassword,
        createdAt: new Date().toISOString(),
        isActive: true
      };

      // In a real implementation, you would save this user to your database
      console.log('User created:', user.id);

      return {
        success: true,
        userId: user.id,
        message: 'Account created successfully'
      };
    } catch (error) {
      console.error('Signup error:', error.message);
      throw error;
    }
  }

  async signin(credentials) {
    try {
      // Rate limiting check
      const identifier = credentials.email.toLowerCase().trim();
      if (this.rateLimiter.isBlocked(identifier)) {
        throw new Error('Too many failed login attempts. Please try again later.');
      }

      // In a real implementation, you would fetch the user from your database
      // For this example, we'll simulate a user lookup
      const user = await this.findUserByEmail(identifier);
      if (!user) {
        // Still record the attempt to prevent enumeration attacks
        this.rateLimiter.recordAttempt(identifier);
        throw new Error('Invalid credentials');
      }

      // Compare passwords
      const isValidPassword = await this.passwordHasher.compare(credentials.password, user.password);
      if (!isValidPassword) {
        this.rateLimiter.recordAttempt(identifier);
        throw new Error('Invalid credentials');
      }

      // Reset rate limit attempts on successful login
      // In a real implementation, you would clear the attempts for this user

      // Create session
      const sessionId = this.sessionManager.createSession(user.id);

      // Generate tokens
      const accessToken = this.tokenManager.generateAccessToken({
        userId: user.id,
        sessionId
      });

      const refreshToken = this.tokenManager.generateRefreshToken({
        userId: user.id,
        sessionId
      });

      return {
        success: true,
        accessToken,
        refreshToken,
        sessionId,
        user: {
          id: user.id,
          email: user.email
        },
        message: 'Login successful'
      };
    } catch (error) {
      console.error('Signin error:', error.message);
      throw error;
    }
  }

  async authenticateRequest(request) {
    try {
      // Extract token from request (header, cookie, etc.)
      const token = this.extractTokenFromRequest(request);
      if (!token) {
        throw new Error('Authentication token required');
      }

      // Verify token
      const decoded = this.tokenManager.verifyToken(token);

      // Check if session is still valid
      const session = this.sessionManager.getSession(decoded.sessionId);
      if (!session || session.userId !== decoded.userId) {
        throw new Error('Invalid session');
      }

      // Extend session
      this.sessionManager.extendSession(decoded.sessionId);

      return {
        authenticated: true,
        userId: decoded.userId,
        sessionId: decoded.sessionId
      };
    } catch (error) {
      console.error('Authentication error:', error.message);
      return {
        authenticated: false,
        error: error.message
      };
    }
  }

  async refreshAccessToken(refreshToken) {
    try {
      // In a real implementation, you would verify the refresh token against your database
      // For this example, we'll just verify the JWT
      
      // Decode the refresh token to get user info
      const decoded = this.tokenManager.verifyToken(refreshToken);
      
      // Check if session is still valid
      const session = this.sessionManager.getSession(decoded.sessionId);
      if (!session || session.userId !== decoded.userId) {
        throw new Error('Invalid session');
      }

      // Generate new access token
      const newAccessToken = this.tokenManager.generateAccessToken({
        userId: decoded.userId,
        sessionId: decoded.sessionId
      });

      return {
        success: true,
        accessToken: newAccessToken
      };
    } catch (error) {
      console.error('Token refresh error:', error.message);
      throw error;
    }
  }

  async logout(sessionId) {
    try {
      // Destroy session
      this.sessionManager.destroySession(sessionId);

      return {
        success: true,
        message: 'Logged out successfully'
      };
    } catch (error) {
      console.error('Logout error:', error.message);
      throw error;
    }
  }

  // Helper method to extract token from request
  extractTokenFromRequest(request) {
    // Check for token in header (Authorization: Bearer <token>)
    if (request.headers && request.headers.authorization) {
      const parts = request.headers.authorization.split(' ');
      if (parts.length === 2 && parts[0] === 'Bearer') {
        return parts[1];
      }
    }

    // Check for token in cookie (if applicable)
    if (request.cookies && request.cookies.authToken) {
      return request.cookies.authToken;
    }

    return null;
  }

  // Simulated user lookup (in real implementation, this would query a database)
  async findUserByEmail(email) {
    // This is a simulation - in a real app, this would query your user database
    // For demo purposes, returning a mock user if email matches a pattern
    if (email === 'test@example.com') {
      return {
        id: 'user_123',
        email: 'test@example.com',
        password: '$2b$12$LQv3c1234567890abcdef', // This would be a real hashed password
        createdAt: '2023-01-01T00:00:00Z',
        isActive: true
      };
    }
    return null;
  }

  // Method to integrate Better Auth if needed
  async setupBetterAuth(config) {
    // This would handle the integration with Better Auth
    // Implementation would depend on Better Auth's specific API
    console.log('Setting up Better Auth with config:', config);
    
    // Return a promise that resolves when setup is complete
    return Promise.resolve({ success: true, message: 'Better Auth configured' });
  }

  // OWASP security checks
  async performSecurityCheck() {
    const issues = [];

    // Check if JWT secret is properly set
    if (!this.config.jwtSecret || this.config.jwtSecret === process.env.JWT_SECRET) {
      issues.push('JWT secret not properly configured');
    }

    // Check password requirements
    if (this.config.passwordMinLength < 8) {
      issues.push('Password minimum length should be at least 8 characters');
    }

    // Check token expiration times
    if (this.config.accessTokenExpiry && 
        (typeof this.config.accessTokenExpiry === 'string' && 
         this.config.accessTokenExpiry.endsWith('h') && 
         parseInt(this.config.accessTokenExpiry) > 24)) {
      issues.push('Access token expiry should be shorter (recommended: less than 24 hours)');
    }

    return {
      secure: issues.length === 0,
      issues
    };
  }
}

module.exports = AuthAgent;
# Environment Configuration for Security Best Practices

## Backend Security Configuration

### JWT and Authentication
# Secret key for JWT signing - MUST BE STRONG AND SECURE
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here-change-in-production

# Token expiration times
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

### Database Security
# Database URL with SSL enabled
DATABASE_URL=postgresql://username:password@localhost/dbname?sslmode=require

### Security Headers
# Allowed hosts for TrustedHostMiddleware
ALLOWED_HOSTS=localhost,127.0.0.1,.vercel.app

# CORS origins - restrict to only required domains
BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:3001,https://yourdomain.com

### Rate Limiting
# Rate limit requests per minute
RATE_LIMIT_REQUESTS_PER_MINUTE=60

### Security Settings
# Enable HTTPS in production
SECURE_SSL_REDIRECT=True

# Security headers
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_CONTENT_TYPE_NOSNIFF=True
SECURE_BROWSER_XSS_PROTECTION=True
SECURE_REFERRER_POLICY=same-origin

## Frontend Security Configuration

### API Configuration
# Base URL for API calls
NEXT_PUBLIC_API_BASE_URL=https://your-backend-domain.com

# Better Auth configuration
NEXT_PUBLIC_BETTER_AUTH_URL=https://your-backend-domain.com/api/auth
NEXT_PUBLIC_JWT_SECRET=your-super-secret-jwt-key-here-change-in-production

### Security Headers (Frontend)
# Content Security Policy (implemented in next.config.js)
# Strict-Transport-Security (handled by backend)
# X-Content-Type-Options (handled by backend)
# X-Frame-Options (handled by backend)
# X-XSS-Protection (handled by backend)

## Production Security Checklist

### Before Going Live
- [ ] Change `BETTER_AUTH_SECRET` to a strong, random value
- [ ] Update `DATABASE_URL` to production database with SSL
- [ ] Verify `ALLOWED_HOSTS` only includes production domains
- [ ] Verify `BACKEND_CORS_ORIGINS` only includes trusted origins
- [ ] Enable HTTPS and SSL redirection
- [ ] Set appropriate rate limits
- [ ] Review all logging levels (reduce to warning/error in production)
- [ ] Disable debug mode
- [ ] Set up monitoring for security events
- [ ] Implement backup and recovery procedures

### Security Monitoring
# Enable detailed logging in staging/development
LOG_LEVEL=INFO

# In production, consider reducing to WARNING or ERROR
PROD_LOG_LEVEL=WARNING

### Secrets Management
# Use a secrets management system in production
# Never commit secrets to version control
# Rotate secrets regularly
# Use different secrets for different environments
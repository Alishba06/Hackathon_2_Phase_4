---
name: auth-skill
description: Implement secure authentication flows including signup, signin, password hashing, JWT tokens, and Better Auth integration.
---

# Auth Skill – Secure Authentication & Authorization

## Instructions

1. **User Signup**
   - Validate input data (email, password, username)
   - Hash passwords securely before storing
   - Prevent duplicate accounts
   - Return clear success/error responses

2. **User Signin**
   - Verify credentials securely
   - Compare hashed passwords
   - Handle invalid login attempts safely
   - Support session-based or token-based auth

3. **Password Hashing**
   - Use strong hashing algorithms (e.g., bcrypt, argon2)
   - Apply proper salt and cost factors
   - Never store plain-text passwords
   - Follow industry security standards

4. **JWT Tokens**
   - Generate access tokens on successful signin
   - Include minimal, safe payload data
   - Set token expiration and refresh strategy
   - Verify and decode tokens for protected routes

5. **Better Auth Integration**
   - Integrate Better Auth for streamlined auth flows
   - Configure providers and secrets securely
   - Use Better Auth helpers for sessions and tokens
   - Ensure compatibility with frontend and backend stacks

## Security & Best Practices
- Enforce strong password rules
- Use HTTPS-only cookies where applicable
- Protect against common attacks (CSRF, XSS, brute-force)
- Separate auth logic from business logic
- Centralize auth middleware for protected routes
- Log auth events carefully (without sensitive data)

## Usage Guidance
Use this skill when:
- Building **authentication systems** for web or API-based apps
- Implementing **secure signup/signin flows**
- Managing **JWT-based authentication**
- Integrating **Better Auth** into modern stacks (Next.js, FastAPI, etc.)
- You need **production-ready auth logic** with best practices

This skill acts as a **security-focused authentication foundation** for full-stack applications.

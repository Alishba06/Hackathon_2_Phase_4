"""
Authentication middleware for the Todo application.

This module implements the authentication middleware that verifies
JWT tokens for all protected endpoints.
"""

from fastapi import Request, HTTPException, status
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from typing import Optional, Callable
import logging
from datetime import datetime
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, JSONResponse

from ..config.security import JWT_SECRET_KEY, JWT_ALGORITHM
from ..models.user import User
from ..services.auth_service import get_user_by_email
from ..utils.jwt_utils import validate_token_signature, validate_token_claims

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip authentication for OPTIONS requests (preflight requests)
        if request.method == "OPTIONS":
            response = await call_next(request)
            return response

        # Define public endpoints that don't require authentication
        # These are paths that should be accessible without authentication
        public_endpoints = [
            "/",
            "/health",
            "/openapi.json",
            "/docs",
            "/redoc",
            "/auth/login",
            "/auth/register",
            "/auth/logout",
            "/auth/me"
        ]

        # Check if the current path is a public endpoint
        # Handle exact matches and paths that start with the endpoint followed by '/'
        # This handles cases like /docs, /docs/oauth2-redirect, /redoc, etc.
        is_public_route = any(
            request.url.path == endpoint or
            request.url.path.startswith(endpoint + "/") or
            (endpoint == "/docs" and request.url.path.startswith("/docs")) or
            (endpoint == "/redoc" and request.url.path.startswith("/redoc"))
            for endpoint in public_endpoints
        )

        # Skip authentication for public endpoints
        if is_public_route:
            response = await call_next(request)
            return response

        # Extract the authorization header
        authorization = request.headers.get("Authorization")
        if not authorization:
            # No authorization header provided
            logger.warning(f"Unauthorized access attempt to {request.url.path}")
            response = JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Not authenticated"},
                headers={"WWW-Authenticate": "Bearer"}
            )
            # Add CORS headers to the response
            response.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin", "*")
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Headers"] = request.headers.get("Access-Control-Request-Headers", "*")
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, PATCH, OPTIONS"
            return response

        # Check if the header has the correct format
        if not authorization.startswith("Bearer "):
            logger.warning(f"Invalid authorization header format for request {request.url.path}")
            response = JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid authorization header format"},
                headers={"WWW-Authenticate": "Bearer"}
            )
            # Add CORS headers to the response
            response.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin", "*")
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Headers"] = request.headers.get("Access-Control-Request-Headers", "*")
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, PATCH, OPTIONS"
            return response

        token = authorization.split(" ")[1]

        # Validate the token signature
        if not validate_token_signature(token):
            logger.warning(f"Invalid token signature for request {request.url.path}")
            response = JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Could not validate credentials"},
                headers={"WWW-Authenticate": "Bearer"}
            )
            # Add CORS headers to the response
            response.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin", "*")
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Headers"] = request.headers.get("Access-Control-Request-Headers", "*")
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, PATCH, OPTIONS"
            return response

        # Validate the token claims
        payload = validate_token_claims(token)
        if payload is None:
            logger.warning(f"Invalid token claims for request {request.url.path}")
            response = JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Could not validate credentials"},
                headers={"WWW-Authenticate": "Bearer"}
            )
            # Add CORS headers to the response
            response.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin", "*")
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Headers"] = request.headers.get("Access-Control-Request-Headers", "*")
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, PATCH, OPTIONS"
            return response

        email: str = payload.get("sub")
        if email is None:
            logger.warning(f"Invalid token: no email found in payload for request {request.url.path}")
            response = JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Could not validate credentials"},
                headers={"WWW-Authenticate": "Bearer"}
            )
            # Add CORS headers to the response
            response.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin", "*")
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Headers"] = request.headers.get("Access-Control-Request-Headers", "*")
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, PATCH, OPTIONS"
            return response

        # Retrieve user from database
        user = get_user_by_email(email)
        if user is None:
            logger.warning(f"Valid token but user not found: {email} for request {request.url.path}")
            response = JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "User not found"},
                headers={"WWW-Authenticate": "Bearer"}
            )
            # Add CORS headers to the response
            response.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin", "*")
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Headers"] = request.headers.get("Access-Control-Request-Headers", "*")
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, PATCH, OPTIONS"
            return response

        # Verify user is active
        if not user.is_active:
            logger.warning(f"Inactive user attempted access: {email} for request {request.url.path}")
            response = JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Inactive user"},
                headers={"WWW-Authenticate": "Bearer"}
            )
            # Add CORS headers to the response
            response.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin", "*")
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Headers"] = request.headers.get("Access-Control-Request-Headers", "*")
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, PATCH, OPTIONS"
            return response

        # Add user info to request state for use in route handlers
        request.state.user = user

        response = await call_next(request)
        return response
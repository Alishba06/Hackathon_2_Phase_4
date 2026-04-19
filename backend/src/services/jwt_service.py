"""JWT Verification Service for AI Chatbot Authentication.

This service handles JWT token verification using Better Auth shared secret.
"""
import os
from typing import Optional, Dict, Any
from jose import jwt, JWTError, ExpiredSignatureError
from pydantic import BaseModel
from datetime import datetime


class JWTPayload(BaseModel):
    """Parsed JWT payload structure."""
    user_id: str
    email: str
    exp: Optional[datetime] = None


class JWTVerificationResult(BaseModel):
    """Result of JWT verification."""
    valid: bool
    user_id: Optional[str] = None
    email: Optional[str] = None
    error: Optional[str] = None


class JWTService:
    """Service for JWT token verification."""
    
    def __init__(self):
        """Initialize JWT service with Better Auth secret."""
        self.secret = os.getenv("BETTER_AUTH_SECRET")
        if not self.secret:
            raise ValueError("BETTER_AUTH_SECRET environment variable is required")
        self.algorithm = "HS256"
    
    def verify_token(self, token: str) -> JWTVerificationResult:
        """
        Verify JWT token and extract user information.
        
        Args:
            token: JWT token string (without 'Bearer ' prefix)
            
        Returns:
            JWTVerificationResult with user info if valid, error if invalid
        """
        try:
            payload = jwt.decode(
                token,
                self.secret,
                algorithms=[self.algorithm],
                options={"verify_exp": True}
            )
            
            user_id = payload.get("user_id")
            email = payload.get("email")
            
            if not user_id:
                return JWTVerificationResult(
                    valid=False,
                    error="user_id not found in token"
                )
            
            return JWTVerificationResult(
                valid=True,
                user_id=user_id,
                email=email or ""
            )
            
        except ExpiredSignatureError:
            return JWTVerificationResult(
                valid=False,
                error="Token has expired"
            )
        except JWTError as e:
            return JWTVerificationResult(
                valid=False,
                error=f"Invalid token: {str(e)}"
            )
        except Exception as e:
            return JWTVerificationResult(
                valid=False,
                error=f"Token verification failed: {str(e)}"
            )
    
    def extract_token_from_header(self, authorization_header: str) -> Optional[str]:
        """
        Extract JWT token from Authorization header.
        
        Args:
            authorization_header: Full Authorization header value
            
        Returns:
            Token string without 'Bearer ' prefix, or None if invalid format
        """
        if not authorization_header:
            return None
            
        parts = authorization_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return None
            
        return parts[1]


# Singleton instance
_jwt_service: Optional[JWTService] = None


def get_jwt_service() -> JWTService:
    """Get or create JWT service singleton."""
    global _jwt_service
    if _jwt_service is None:
        _jwt_service = JWTService()
    return _jwt_service

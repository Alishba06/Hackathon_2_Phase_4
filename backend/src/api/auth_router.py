from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from typing import Dict
import logging

from ..models.user import User, UserCreate
from ..models.auth import UserResponse
from ..services.auth_service import authenticate_user, create_user
from ..utils.jwt_utils import create_access_token
from ..utils.security import hash_password
from ..config.database import engine
from ..services.logging_service import log_authentication_success, log_authentication_failure
from ..api.deps import get_current_active_user
from pydantic import BaseModel

# Define a model for the login request
class LoginRequest(BaseModel):
    email: str
    password: str

router = APIRouter(prefix="/auth", tags=["authentication"])

# Set up logging
logger = logging.getLogger(__name__)

def get_session():
    with Session(engine) as session:
        yield session

@router.post("/login", response_model=Dict[str, str])
def login_json(login_request: LoginRequest, session: Session = Depends(get_session)):
    """
    Authenticate user and return JWT token (accepts JSON).
    """
    try:
        user = authenticate_user(login_request.email, login_request.password)

        if not user:
            # Log authentication failure
            log_authentication_failure(
                email=login_request.email,
                ip_address=None,  # Would come from request object in a real implementation
                user_agent=None   # Would come from request object in a real implementation
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Log authentication success
        log_authentication_success(
            user=user,
            ip_address=None,  # Would come from request object in a real implementation
            user_agent=None   # Would come from request object in a real implementation
        )

        # Create access token - convert UUID to string for JSON serialization
        access_token = create_access_token(data={"sub": user.email, "user_id": str(user.id)})

        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Handle any other unexpected errors
        logger.error(f"Authentication error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during authentication"
        )


@router.post("/login-form", response_model=Dict[str, str])
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    """
    Authenticate user and return JWT token (accepts form data).
    """
    try:
        user = authenticate_user(form_data.username, form_data.password)

        if not user:
            # Log authentication failure
            log_authentication_failure(
                email=form_data.username,
                ip_address=None,  # Would come from request object in a real implementation
                user_agent=None   # Would come from request object in a real implementation
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Log authentication success
        log_authentication_success(
            user=user,
            ip_address=None,  # Would come from request object in a real implementation
            user_agent=None   # Would come from request object in a real implementation
        )

        # Create access token - convert UUID to string for JSON serialization
        access_token = create_access_token(data={"sub": user.email, "user_id": str(user.id)})

        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Handle any other unexpected errors
        logger.error(f"Authentication error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during authentication"
        )


class RegisterResponse(BaseModel):
    """Response model for registration endpoint"""
    id: str
    email: str
    first_name: str | None
    last_name: str | None
    created_at: str
    access_token: str
    token_type: str = "bearer"

@router.post("/register", response_model=RegisterResponse)
def register(user_create: UserCreate, session: Session = Depends(get_session)):
    """
    Register a new user and return user info with access token.
    """
    try:
        # Validate password is not empty
        if not user_create.password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password cannot be empty"
            )

        # Hash the password using our secure utility
        try:
            hashed_password = hash_password(user_create.password)
        except ValueError as ve:
            logger.error(f"Password hashing error: {str(ve)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Password hashing failed: {str(ve)}"
            )

        # Check if user already exists
        from sqlmodel import select
        existing_user = session.exec(select(User).where(User.email == user_create.email)).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists"
            )

        # Create the user object
        user = User(
            email=user_create.email,
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            password_hash=hashed_password
        )

        # Save to database
        session.add(user)
        session.commit()
        session.refresh(user)

        # Create access token - convert UUID to string for JSON serialization
        access_token = create_access_token(data={"sub": user.email, "user_id": str(user.id)})

        # Return user response with token - ensure ID is string
        return RegisterResponse(
            id=str(user.id),
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            created_at=str(user.created_at),
            access_token=access_token,
            token_type="bearer"
        )
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log the exception for debugging
        logger.error(f"Registration error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration"
        )


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_active_user)):
    """
    Get the current authenticated user's profile information.
    """
    try:
        return UserResponse(
            id=str(current_user.id),
            email=current_user.email,
            first_name=current_user.first_name,
            last_name=current_user.last_name,
            created_at=str(current_user.created_at)
        )
    except Exception as e:
        logger.error(f"Get user profile error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving user profile"
        )


@router.post("/logout")
def logout():
    """
    Logout the current user.
    Note: Since JWT tokens are stateless, we can't actually invalidate the token server-side.
    In a real application, you might implement a token blacklist mechanism.
    For now, this endpoint serves as a placeholder for frontend logout logic.
    """
    return {"message": "Successfully logged out"}
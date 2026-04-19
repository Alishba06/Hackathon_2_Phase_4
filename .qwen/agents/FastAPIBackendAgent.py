"""
FastAPI Backend Agent

Focus: Ownership of everything related to the FastAPI backend, ensuring a robust, 
secure, and well-structured REST API layer.

This agent is responsible for designing, implementing, reviewing, and improving 
FastAPI backend services without breaking existing functionality.
"""

import asyncio
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, ValidationError
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import jwt
from datetime import datetime, timedelta
import logging
import os
from enum import Enum


class FastAPIBackendAgent:
    """
    FastAPI Backend Agent - Manages FastAPI backend services with focus on
    robustness, security, and maintainability.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.app: Optional[FastAPI] = None
        self.security = HTTPBearer()
        self.logger = self._setup_logger()
        self.db_connection = None
        
        # Initialize default settings
        self.jwt_secret = self.config.get('jwt_secret', os.getenv('JWT_SECRET', 'default-secret'))
        self.jwt_algorithm = self.config.get('jwt_algorithm', 'HS256')
        self.access_token_expire_minutes = self.config.get('access_token_expire_minutes', 30)
        self.refresh_token_expire_days = self.config.get('refresh_token_expire_days', 7)
        
    def _setup_logger(self):
        """Setup logger for the agent"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        """Lifespan manager for FastAPI application"""
        # Startup
        self.logger.info("Starting up FastAPI Backend Agent...")
        self.db_connection = await self._initialize_database()
        
        yield
        
        # Shutdown
        self.logger.info("Shutting down FastAPI Backend Agent...")
        if self.db_connection:
            await self._close_database()

    def create_app(self, title: str = "FastAPI Backend Service", 
                   version: str = "1.0.0", 
                   description: str = "Robust and secure FastAPI backend service") -> FastAPI:
        """Create a FastAPI application with recommended settings"""
        
        # Create FastAPI app with lifespan
        self.app = FastAPI(
            title=title,
            version=version,
            description=description,
            lifespan=self.lifespan
        )
        
        # Add CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=self.config.get('allow_origins', ["*"]),
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Add security middleware
        self._add_security_middlewares()
        
        # Add routes
        self._add_default_routes()
        
        return self.app

    def _add_security_middlewares(self):
        """Add security middlewares to the application"""
        # Add custom security headers
        @self.app.middleware("http")
        async def add_security_headers(request: Request, call_next):
            response = await call_next(request)
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["X-XSS-Protection"] = "1; mode=block"
            return response

    def _add_default_routes(self):
        """Add default routes to the application"""
        
        # Health check endpoint
        @self.app.get("/health", tags=["System"])
        async def health_check():
            return {"status": "healthy", "timestamp": datetime.utcnow()}
        
        # API info endpoint
        @self.app.get("/info", tags=["System"])
        async def api_info():
            return {
                "title": self.app.title,
                "version": self.app.version,
                "description": self.app.description,
                "timestamp": datetime.utcnow()
            }

    async def _initialize_database(self):
        """Initialize database connection"""
        # This is a placeholder - in a real implementation, 
        # this would connect to the actual database
        self.logger.info("Initializing database connection...")
        # Simulate async database initialization
        await asyncio.sleep(0.1)
        return {"connected": True, "engine": "mock_db"}

    async def _close_database(self):
        """Close database connection"""
        self.logger.info("Closing database connection...")
        # Simulate closing connection
        await asyncio.sleep(0.05)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.jwt_secret, algorithm=self.jwt_algorithm)
        return encoded_jwt

    def create_refresh_token(self, data: dict):
        """Create JWT refresh token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, self.jwt_secret, algorithm=self.jwt_algorithm)
        return encoded_jwt

    def verify_token(self, token: str):
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    async def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(security)):
        """Get current user from token"""
        token = credentials.credentials
        payload = self.verify_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"user_id": user_id}

    def add_authentication_routes(self):
        """Add authentication routes to the application"""
        
        class Token(BaseModel):
            access_token: str
            refresh_token: str
            token_type: str = "bearer"

        class LoginRequest(BaseModel):
            username: str = Field(..., min_length=3, max_length=50)
            password: str = Field(..., min_length=8)

        @self.app.post("/auth/login", response_model=Token, tags=["Authentication"])
        async def login(request: LoginRequest):
            # This is a placeholder - in a real implementation,
            # this would validate credentials against a database
            user_id = request.username  # Simplified for example
            
            # Create tokens
            access_token = self.create_access_token(data={"sub": user_id})
            refresh_token = self.create_refresh_token(data={"sub": user_id})
            
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"
            }

        @self.app.post("/auth/refresh", response_model=Token, tags=["Authentication"])
        async def refresh_token(refresh_token: str):
            payload = self.verify_token(refresh_token)
            if payload.get("type") != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token type",
                )
            
            # Create new access token
            new_access_token = self.create_access_token(data={"sub": payload.get("sub")})
            new_refresh_token = self.create_refresh_token(data={"sub": payload.get("sub")})
            
            return {
                "access_token": new_access_token,
                "refresh_token": new_refresh_token,
                "token_type": "bearer"
            }

    def add_crud_routes(self, model_name: str, schema: BaseModel, db_operations=None):
        """Add CRUD routes for a specific model"""
        
        # Define path for the model
        model_path = f"/{model_name.lower()}s"
        
        # GET all items
        @self.app.get(model_path, tags=[model_name])
        async def get_items(skip: int = 0, limit: int = 100):
            if db_operations and hasattr(db_operations, 'get_items'):
                return await db_operations.get_items(skip=skip, limit=limit)
            else:
                # Mock response
                return [{"id": i, "name": f"Item {i}"} for i in range(skip, skip + limit)]

        # GET single item
        @self.app.get(f"{model_path}/{{item_id}}", tags=[model_name])
        async def get_item(item_id: int):
            if db_operations and hasattr(db_operations, 'get_item'):
                return await db_operations.get_item(item_id)
            else:
                # Mock response
                return {"id": item_id, "name": f"Item {item_id}"}

        # POST create item
        @self.app.post(model_path, tags=[model_name])
        async def create_item(item: schema):
            if db_operations and hasattr(db_operations, 'create_item'):
                return await db_operations.create_item(item)
            else:
                # Mock response
                return {"id": 1, **item.dict()}

        # PUT update item
        @self.app.put(f"{model_path}/{{item_id}}", tags=[model_name])
        async def update_item(item_id: int, item: schema):
            if db_operations and hasattr(db_operations, 'update_item'):
                return await db_operations.update_item(item_id, item)
            else:
                # Mock response
                return {"id": item_id, **item.dict()}

        # DELETE item
        @self.app.delete(f"{model_path}/{{item_id}}", tags=[model_name])
        async def delete_item(item_id: int):
            if db_operations and hasattr(db_operations, 'delete_item'):
                return await db_operations.delete_item(item_id)
            else:
                # Mock response
                return {"id": item_id, "deleted": True}

    def add_error_handlers(self):
        """Add global error handlers to the application"""
        
        @self.app.exception_handler(ValidationError)
        async def validation_exception_handler(request: Request, exc: ValidationError):
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={
                    "detail": "Validation error",
                    "errors": exc.errors()
                }
            )

        @self.app.exception_handler(HTTPException)
        async def http_exception_handler(request: Request, exc: HTTPException):
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "detail": exc.detail
                }
            )

        @self.app.exception_handler(Exception)
        async def general_exception_handler(request: Request, exc: Exception):
            self.logger.error(f"Unhandled exception: {str(exc)}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "detail": "Internal server error"
                }
            )

    def add_pagination_support(self):
        """Add pagination support utilities"""
        
        class PaginationParams(BaseModel):
            skip: int = Field(0, ge=0, description="Number of records to skip")
            limit: int = Field(100, ge=1, le=1000, description="Maximum number of records to return")

        # This would be used as a dependency in routes that need pagination
        def pagination_params(skip: int = 0, limit: int = 100) -> PaginationParams:
            return PaginationParams(skip=skip, limit=limit)

        return pagination_params

    def add_rate_limiting(self, max_requests: int = 100, window_seconds: int = 60):
        """Add rate limiting to the application"""
        # This is a simplified implementation
        # In a real application, you'd use a more sophisticated solution like slowapi
        from collections import defaultdict
        import time
        
        request_counts = defaultdict(list)
        
        @self.app.middleware("http")
        async def rate_limit_middleware(request: Request, call_next):
            client_ip = request.client.host
            now = time.time()
            
            # Clean old requests
            request_counts[client_ip] = [
                req_time for req_time in request_counts[client_ip] 
                if now - req_time < window_seconds
            ]
            
            # Check if limit exceeded
            if len(request_counts[client_ip]) >= max_requests:
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={"detail": "Rate limit exceeded"}
                )
            
            # Add current request
            request_counts[client_ip].append(now)
            
            response = await call_next(request)
            return response

    def validate_request_schema(self, schema: BaseModel, data: Dict[str, Any]) -> BaseModel:
        """Validate request data against a Pydantic schema"""
        try:
            validated_data = schema(**data)
            return validated_data
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=e.errors()
            )

    def add_cors_configuration(self, allow_origins: List[str], 
                             allow_credentials: bool = True,
                             allow_methods: List[str] = ["*"],
                             allow_headers: List[str] = ["*"]):
        """Add CORS configuration to the application"""
        # Remove existing CORS middleware if any
        self.app.user_middleware = [
            m for m in self.app.user_middleware 
            if m.cls.__name__ != 'CORSMiddleware'
        ]
        
        # Add new CORS middleware with specified configuration
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=allow_origins,
            allow_credentials=allow_credentials,
            allow_methods=allow_methods,
            allow_headers=allow_headers,
        )

    def get_application(self) -> FastAPI:
        """Get the FastAPI application instance"""
        if not self.app:
            raise ValueError("Application not created. Call create_app() first.")
        return self.app


# Example usage and testing
if __name__ == "__main__":
    # Example of how to use the FastAPI Backend Agent
    
    # Define a sample model
    class User(BaseModel):
        id: Optional[int] = None
        name: str = Field(..., min_length=1, max_length=100)
        email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
        age: Optional[int] = Field(None, ge=0, le=150)

    # Initialize the agent
    agent = FastAPIBackendAgent({
        'jwt_secret': 'my-super-secret-key',
        'allow_origins': ['http://localhost:3000']
    })
    
    # Create the application
    app = agent.create_app(
        title="User Management API",
        version="1.0.0",
        description="API for managing users"
    )
    
    # Add authentication routes
    agent.add_authentication_routes()
    
    # Add CRUD routes for User model
    agent.add_crud_routes("User", User)
    
    # Add error handlers
    agent.add_error_handlers()
    
    # Add rate limiting
    agent.add_rate_limiting(max_requests=50, window_seconds=60)
    
    # Get the application instance
    application = agent.get_application()
    
    # Run the application (uncomment to actually run)
    # import uvicorn
    # uvicorn.run(application, host="0.0.0.0", port=8000)
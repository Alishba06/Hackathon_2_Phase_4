from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from sqlmodel import SQLModel
import os
from dotenv import load_dotenv

from src.api.task_router import router as task_router
from src.api.auth_router import router as auth_router
from src.api.chat_router import router as chat_router
from src.config.database import engine

# Import all models to register them with SQLModel metadata
# Import in a specific order to handle circular dependencies
from src.models.user import User
from src.models.task import Task
from src.models.security_log import SecurityLog
from src.models.conversation import Conversation
from src.models.message import Message

from src.middleware.auth_middleware import AuthMiddleware

# Load the corrected environment file
load_dotenv(dotenv_path="../../.env")

app = FastAPI(title="Todo API", version="2.0.0")

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://localhost:8000",  # Allow same-origin requests during development
        "http://127.0.0.1:8000",  # Backend address for direct testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose authorization header to frontend
    expose_headers=["Access-Control-Allow-Origin", "Authorization"]
)

# ✅ Auth middleware
app.add_middleware(AuthMiddleware)

# ✅ Trusted hosts
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1"]
)

# ✅ Routers
app.include_router(auth_router, prefix="", tags=["authentication"])
app.include_router(task_router, prefix="/api", tags=["tasks"])
app.include_router(chat_router, prefix="/api", tags=["chat"])

@app.on_event("startup")
async def startup():
    # Ensure all models are registered before creating tables
    SQLModel.metadata.create_all(engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API - Phase III AI Chatbot"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}













# from fastapi import FastAPI, Depends
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.middleware.trustedhost import TrustedHostMiddleware
# from src.api.task_router import router as task_router
# from src.api.auth_router import router as auth_router
# from src.config.database import engine
# from sqlmodel import SQLModel
# import os
# from dotenv import load_dotenv

# # Import models to register them with SQLModel metadata
# from src.models.user import User
# from src.models.task import Task
# from src.models.security_log import SecurityLog

# # Import middleware
# from src.middleware.auth_middleware import AuthMiddleware

# load_dotenv()

# # Create the FastAPI app
# app = FastAPI(title="Todo API", version="1.0.0")

# # Add CORS middleware FIRST (before any other middleware that might interfere)
# import ast
# cors_origins_str = os.getenv("BACKEND_CORS_ORIGINS", '["http://localhost:3000", "http://localhost:3001"]')
# try:
#     origins = ast.literal_eval(cors_origins_str)
#     if not isinstance(origins, list):
#         origins = ["http://localhost:3000", "http://localhost:3001"]
# except (ValueError, SyntaxError):
#     origins = ["http://localhost:3000", "http://localhost:3001"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],  # Use the parsed origins list
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Add authentication middleware AFTER CORS middleware
# app.add_middleware(AuthMiddleware)

# # Add trusted host middleware
# allowed_hosts_str = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1")
# allowed_hosts = [host.strip() for host in allowed_hosts_str.split(",")]
# app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)

# # Include the auth router (at root level to match frontend expectations)
# app.include_router(auth_router, prefix="", tags=["authentication"])

# # Include the task router
# app.include_router(task_router, prefix="/api", tags=["tasks"])

# @app.on_event("startup")
# async def startup():
#     # Create database tables
#     SQLModel.metadata.create_all(engine)

# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the Todo API"}

# @app.get("/health")
# def health_check():
#     return {"status": "healthy"}
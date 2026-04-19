from fastapi import APIRouter, Depends, HTTPException, Path, Request
from sqlmodel import Session
from typing import List
from src.services.task_service import TaskService
from src.models.task import Task, TaskCreate, TaskUpdate
from src.models.user import User
from src.config.database import engine
from src.api.deps import get_current_user
from src.services.logging_service import log_unauthorized_access, log_user_isolation_violation
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(tags=["tasks"])

# Dependency to get database session
def get_session():
    with Session(engine) as session:
        yield session

@router.get("/tasks", response_model=List[Task])
def get_tasks(
    request: Request,
    completed: bool = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user, optionally filtered by completion status.
    """
    # Use the current user's ID from the JWT token, not from the URL
    tasks = TaskService.get_tasks_by_user_id(session=session, user_id=current_user.id, completed=completed)
    return tasks

@router.post("/tasks", response_model=Task)
def create_task(
    request: Request,
    task_create: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.
    """
    # Use the current user's ID from the JWT token, not from the URL
    task = TaskService.create_task(session=session, task_create=task_create, user_id=current_user.id)
    return task

@router.get("/tasks/{task_id}", response_model=Task)
def get_task(
    request: Request,
    task_id: str = Path(...),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID for the authenticated user.
    """
    # Use the current user's ID from the JWT token, not from the URL
    task = TaskService.get_task_by_id_and_user_id(session=session, task_id=task_id, user_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=Task)
def update_task(
    request: Request,
    task_id: str = Path(...),
    task_update: TaskUpdate = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific task for the authenticated user.
    """
    # Use the current user's ID from the JWT token, not from the URL
    db_task = TaskService.get_task_by_id_and_user_id(session=session, task_id=task_id, user_id=current_user.id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Verify that the task belongs to the current user
    if db_task.user_id != current_user.id:
        # Log the user isolation violation
        log_user_isolation_violation(
            accessing_user_id=current_user.id,
            target_user_id=db_task.user_id,
            endpoint=f"/tasks/{task_id}",
            ip_address=request.client.host if hasattr(request, 'client') else None,
            user_agent=request.headers.get('user-agent', None)
        )
        logger.warning(f"User {current_user.id} attempted to update task {task_id} of user {db_task.user_id}")
        raise HTTPException(status_code=403, detail="Not authorized to update this task")

    updated_task = TaskService.update_task(session=session, db_task=db_task, task_update=task_update)
    return updated_task

@router.delete("/tasks/{task_id}")
def delete_task(
    request: Request,
    task_id: str = Path(...),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task for the authenticated user.
    """
    # Use the current user's ID from the JWT token, not from the URL
    db_task = TaskService.get_task_by_id_and_user_id(session=session, task_id=task_id, user_id=current_user.id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Verify that the task belongs to the current user
    if db_task.user_id != current_user.id:
        # Log the user isolation violation
        log_user_isolation_violation(
            accessing_user_id=current_user.id,
            target_user_id=db_task.user_id,
            endpoint=f"/tasks/{task_id}",
            ip_address=request.client.host if hasattr(request, 'client') else None,
            user_agent=request.headers.get('user-agent', None)
        )
        logger.warning(f"User {current_user.id} attempted to delete task {task_id} of user {db_task.user_id}")
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")

    TaskService.delete_task(session=session, db_task=db_task)
    return {"message": "Task deleted successfully"}

@router.patch("/tasks/{task_id}", response_model=Task)
def update_task_partially(
    request: Request,
    task_id: str = Path(...),
    task_update: TaskUpdate = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Partially update a specific task for the authenticated user (e.g., toggle completion status).
    """
    # Use the current user's ID from the JWT token, not from the URL
    db_task = TaskService.get_task_by_id_and_user_id(session=session, task_id=task_id, user_id=current_user.id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Verify that the task belongs to the current user
    if db_task.user_id != current_user.id:
        # Log the user isolation violation
        log_user_isolation_violation(
            accessing_user_id=current_user.id,
            target_user_id=db_task.user_id,
            endpoint=f"/tasks/{task_id}",
            ip_address=request.client.host if hasattr(request, 'client') else None,
            user_agent=request.headers.get('user-agent', None)
        )
        logger.warning(f"User {current_user.id} attempted to update task {task_id} of user {db_task.user_id}")
        raise HTTPException(status_code=403, detail="Not authorized to update this task")

    updated_task = TaskService.update_task(session=session, db_task=db_task, task_update=task_update)
    return updated_task
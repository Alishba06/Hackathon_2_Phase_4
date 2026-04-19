from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=10000)
    is_completed: bool = False
    due_date: Optional[datetime] = None
    priority: Optional[str] = Field(default='medium', regex='^(low|medium|high)$')

class Task(TaskBase, table=True):
    id: str = Field(default_factory=generate_uuid, primary_key=True)
    user_id: str = Field(index=True, foreign_key="user.id", max_length=36)  # Added index for performance, UUID is 36 chars
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Additional validation to enforce user ownership
    def belongs_to_user(self, user_id: str) -> bool:
        """
        Check if this task belongs to the specified user.

        Args:
            user_id: ID of the user to check ownership against

        Returns:
            True if the task belongs to the user, False otherwise
        """
        return self.user_id == user_id

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = None

class TaskOwnershipError(Exception):
    """
    Exception raised when a user attempts to access a task that doesn't belong to them.
    """
    def __init__(self, user_id: str, task_id: str):
        self.user_id = user_id
        self.task_id = task_id
        super().__init__(f"User {user_id} does not own task {task_id}")
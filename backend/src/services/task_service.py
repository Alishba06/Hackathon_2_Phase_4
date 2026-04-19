from sqlmodel import Session, select
from src.models.task import Task, TaskCreate, TaskUpdate
from src.models.user import User
from typing import List, Optional
from datetime import datetime

class TaskService:
    @staticmethod
    def create_task(*, session: Session, task_create: TaskCreate, user_id: str) -> Task:
        """
        Create a new task for a specific user
        """
        # Convert Pydantic model to dict using model_dump for compatibility
        task_data = task_create.model_dump()
        db_task = Task(**task_data)
        db_task.user_id = user_id
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task

    @staticmethod
    def get_tasks_by_user_id(*, session: Session, user_id: str, completed: Optional[bool] = None) -> List[Task]:
        """
        Get all tasks for a specific user, optionally filtered by completion status
        """
        query = select(Task).where(Task.user_id == user_id)

        if completed is not None:
            query = query.where(Task.is_completed == completed)

        tasks = session.exec(query).all()
        return tasks

    @staticmethod
    def get_task_by_id_and_user_id(*, session: Session, task_id: str, user_id: str) -> Optional[Task]:
        """
        Get a specific task by its ID and user ID to ensure user isolation
        """
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(query).first()
        return task

    @staticmethod
    def update_task(*, session: Session, db_task: Task, task_update: TaskUpdate) -> Task:
        """
        Update a task with the provided values
        """
        # Use model_dump for compatibility with newer Pydantic versions
        for field, value in task_update.model_dump(exclude_unset=True).items():
            setattr(db_task, field, value)

        db_task.updated_at = datetime.utcnow()
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task

    @staticmethod
    def delete_task(*, session: Session, db_task: Task) -> None:
        """
        Delete a task
        """
        session.delete(db_task)
        session.commit()

    @staticmethod
    def toggle_task_completion(*, session: Session, db_task: Task, is_completed: bool) -> Task:
        """
        Toggle the completion status of a task
        """
        db_task.is_completed = is_completed
        db_task.updated_at = datetime.utcnow()
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task
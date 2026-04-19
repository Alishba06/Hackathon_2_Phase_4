---
name: backend-core
description: Generate backend routes, handle requests/responses, and connect databases for scalable web applications.
---

# Backend Skill – API, Routing & Database Integration

## Instructions

1. **Route Generation**
   - Create RESTful or RPC-style routes
   - Follow clear URL naming conventions
   - Separate routes by resource/module
   - Support CRUD operations (Create, Read, Update, Delete)

2. **Request & Response Handling**
   - Validate incoming request data
   - Handle query params, path params, and request bodies
   - Return consistent JSON responses
   - Use proper HTTP status codes
   - Implement error handling and meaningful error messages

3. **Database Connectivity**
   - Connect to databases (SQL / NoSQL)
   - Manage database sessions and connections efficiently
   - Perform secure queries and transactions
   - Map data models to database schemas
   - Handle migrations and schema changes safely

4. **Business Logic Layer**
   - Keep route handlers thin
   - Move logic to service/controller layers
   - Reuse logic across multiple routes
   - Ensure scalability and maintainability

## Best Practices
- Use environment variables for secrets and DB credentials
- Validate data using schemas (e.g., Pydantic, Zod)
- Prevent SQL injection and insecure queries
- Log errors and important events
- Keep responses predictable and documented
- Design APIs to be frontend-friendly

## Example Structure
```python
# routes/tasks.py
from fastapi import APIRouter, HTTPException
from models import Task
from database import db

router = APIRouter()

@router.post("/tasks")
async def create_task(task: Task):
    new_task = await db.insert(task)
    return {"success": True, "data": new_task}

@router.get("/tasks/{task_id}")
async def get_task(task_id: int):
    task = await db.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"success": True, "data": task}

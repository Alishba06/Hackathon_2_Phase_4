# Data Model: AI-Powered Todo Chatbot

**Feature**: 004-ai-todo-chatbot
**Date**: 2026-03-27
**Purpose**: Define database entities for conversation and message persistence

---

## New Entities

### Conversation

Represents a chat session belonging to a user. Contains multiple messages and persists across sessions.

**Fields**:
- `id` (UUID, Primary Key): Unique identifier for the conversation
- `user_id` (UUID, Foreign Key → User.id): Owner of the conversation
- `created_at` (DateTime): When the conversation was created
- `updated_at` (DateTime): Last message timestamp (updated on each new message)

**Relationships**:
- Belongs to one User (many-to-one)
- Has many Messages (one-to-many)

**Validation Rules**:
- user_id MUST be a valid UUID referencing an existing User
- updated_at MUST be >= created_at
- Each conversation MUST belong to exactly one user

**State Transitions**:
- Created: When user sends first message to chat endpoint
- Updated: When new message is added to conversation
- (Optional) Archived: Future enhancement for old conversations

---

### Message

Represents a single exchange in a conversation. Can be from user or assistant.

**Fields**:
- `id` (UUID, Primary Key): Unique identifier for the message
- `conversation_id` (UUID, Foreign Key → Conversation.id): Parent conversation
- `user_id` (UUID, Foreign Key → User.id): Message owner (for user isolation)
- `role` (String): "user" or "assistant"
- `content` (Text): Message content
- `created_at` (DateTime): When the message was created

**Relationships**:
- Belongs to one Conversation (many-to-one)
- Belongs to one User (many-to-one)

**Validation Rules**:
- conversation_id MUST reference an existing Conversation
- user_id MUST match the conversation's user_id (enforced at application layer)
- role MUST be either "user" or "assistant"
- content MUST NOT be empty
- content length MUST NOT exceed 10,000 characters

**State Transitions**:
- Created: When user sends message or assistant responds
- (Immutable after creation - no updates allowed)

---

## Existing Entities (Reused)

### Task

Already defined in Phase II. No changes required.

**Fields**: id, user_id, title, description, is_completed, due_date, priority, created_at, updated_at

**Relationships**:
- Belongs to one User (many-to-one)

**Usage in Chatbot**:
- Created, updated, deleted via MCP tools based on user intent
- Always filtered by user_id for isolation

---

### User

Already defined in Phase II. No changes required.

**Fields**: id, email, password_hash, first_name, last_name, is_active, created_at, updated_at, last_login, failed_login_attempts, locked_until

**Relationships**:
- Has many Conversations (one-to-many)
- Has many Messages (one-to-many)
- Has many Tasks (one-to-many)

---

## Entity Relationship Diagram

```
┌─────────────┐
│    User     │
│             │
│ id (PK)     │
│ email       │
│ ...         │
└──────┬──────┘
       │
       ├──────────────────┬──────────────────┐
       │                  │                  │
       ▼                  ▼                  ▼
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│Conversation │   │  Message    │   │    Task     │
│             │   │             │   │             │
│ id (PK)     │   │ id (PK)     │   │ id (PK)     │
│ user_id(FK) │   │ conv_id(FK) │   │ user_id(FK) │
│ created_at  │   │ user_id(FK) │   │ title       │
│ updated_at  │   │ role        │   │ description │
└─────────────┘   │ content     │   │ is_completed│
                  │ created_at  │   │ ...         │
                  └─────────────┘   └─────────────┘
```

---

## SQLModel Definitions

### Conversation Model

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import List, TYPE_CHECKING
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class ConversationBase(SQLModel):
    pass

class Conversation(ConversationBase, table=True):
    __tablename__ = "conversation"
    
    id: str = Field(default_factory=generate_uuid, primary_key=True, max_length=36)
    user_id: str = Field(foreign_key="user.id", index=True, max_length=36)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation")
```

### Message Model

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional, TYPE_CHECKING
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class MessageBase(SQLModel):
    role: str = Field(regex="^(user|assistant)$")
    content: str = Field(min_length=1, max_length=10000)

class Message(MessageBase, table=True):
    __tablename__ = "message"
    
    id: str = Field(default_factory=generate_uuid, primary_key=True, max_length=36)
    conversation_id: str = Field(foreign_key="conversation.id", index=True, max_length=36)
    user_id: str = Field(foreign_key="user.id", index=True, max_length=36)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship to conversation
    conversation: "Conversation" = Relationship(back_populates="messages")
```

---

## Database Indexes

### Performance Optimizations

**Conversation Table**:
- Index on `user_id`: Fast lookup of user's conversations
- Index on `updated_at`: Sort conversations by last activity

**Message Table**:
- Index on `conversation_id`: Fast lookup of conversation messages
- Index on `user_id`: User-scoped message queries
- Composite index on `(conversation_id, created_at)`: Ordered message retrieval

---

## Migration Strategy

### Adding Conversation and Message Tables

1. Create Alembic migration for new tables
2. Add foreign key constraints with ON DELETE CASCADE
3. Create indexes for performance
4. Test migration on development database
5. Apply to production database

### Backward Compatibility

- Existing Task and User models unchanged
- No breaking changes to Phase II functionality
- Chat feature additive to existing todo management

---

## Data Integrity Rules

1. **User Isolation**: All queries MUST filter by user_id
2. **Foreign Key Integrity**: All relationships enforced at database level
3. **Cascade Deletes**: Deleting a user deletes all their conversations and messages
4. **Immutable Messages**: Messages cannot be updated after creation
5. **Conversation Ownership**: Message user_id must match conversation user_id

---

## Query Patterns

### Get User's Conversations

```python
select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc())
```

### Get Conversation Messages

```python
select(Message).where(
    Message.conversation_id == conversation_id,
    Message.user_id == user_id
).order_by(Message.created_at.asc())
```

### Create Message

```python
message = Message(
    conversation_id=conversation_id,
    user_id=user_id,
    role="user",
    content=user_message
)
session.add(message)
session.commit()
```

### Update Conversation Timestamp

```python
conversation.updated_at = datetime.utcnow()
session.add(conversation)
session.commit()
```

"""
TaskAPI - A simple REST API for managing personal tasks.
This file contains the entire API.
Run with: uvicorn main:app --reload --port 8001
Docs: http://127.0.0.1:8001/docs
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
from datetime import datetime

# Create the FastAPI application
app = FastAPI(
    title="TaskAPI",
    description="A simple API to manage personal tasks. Built for One Day · One Build - Day 02",
    version="1.0.0"
)

# Database file
DB_FILE = "tasks.db"

# Pydantic models - these define the shape of data we accept and return
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: str

# Database helper functions
def get_db_connection():
    """Create a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # This lets us access columns by name
    return conn

def init_db():
    """Create the tasks table if it doesn't exist."""
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            completed BOOLEAN NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Initialize the database when the app starts
init_db()

# Root endpoint - just a welcome message
@app.get("/")
def read_root():
    return {
        "message": "Welcome to TaskAPI",
        "docs": "/docs",
        "version": "1.0.0"
    }

# CREATE - Add a new task
@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskCreate):
    """Create a new task."""
    conn = get_db_connection()
    cursor = conn.cursor()
    created_at = datetime.now().isoformat()
    
    cursor.execute(
        "INSERT INTO tasks (title, description, completed, created_at) VALUES (?, ?, ?, ?)",
        (task.title, task.description, False, created_at)
    )
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    
    return Task(
        id=task_id,
        title=task.title,
        description=task.description,
        completed=False,
        created_at=created_at
    )

# READ all - Get all tasks
@app.get("/tasks", response_model=List[Task])
def get_tasks():
    """Get all tasks."""
    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    conn.close()
    
    return [
        Task(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            completed=bool(row["completed"]),
            created_at=row["created_at"]
        )
        for row in tasks
    ]

# READ one - Get a single task by ID
@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    """Get one task by its ID."""
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    
    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return Task(
        id=row["id"],
        title=row["title"],
        description=row["description"],
        completed=bool(row["completed"]),
        created_at=row["created_at"]
    )

# UPDATE - Update a task
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate):
    """Update an existing task."""
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    
    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Use new values if provided, otherwise keep old ones
    title = task_update.title if task_update.title is not None else row["title"]
    description = task_update.description if task_update.description is not None else row["description"]
    completed = task_update.completed if task_update.completed is not None else bool(row["completed"])
    
    conn.execute(
        "UPDATE tasks SET title = ?, description = ?, completed = ? WHERE id = ?",
        (title, description, completed, task_id)
    )
    conn.commit()
    conn.close()
    
    return Task(
        id=task_id,
        title=title,
        description=description,
        completed=completed,
        created_at=row["created_at"]
    )

# DELETE - Delete a task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Delete a task."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"message": "Task deleted successfully", "id": task_id}

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Task Manager API")

class Task(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False

tasks_db = [
    {"id": 1, "title": "Setup Cloud Server", "description": "Configure AWS EC2 instance", "completed": False},
    {"id": 2, "title": "Database Migration", "description": "Migrate user tables to MySQL", "completed": True}
]

@app.get("/tasks", response_model=List[Task])
def get_all_tasks():
    return tasks_db

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    tasks_db.append(task.dict())
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    for index, task in enumerate(tasks_db):
        if task["id"] == task_id:
            tasks_db[index] = updated_task.dict()
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for index, task in enumerate(tasks_db):
        if task["id"] == task_id:
            tasks_db.pop(index)
            return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app= FastAPI(title="Task Scheduler API")

task=[]

class TaskCreate(BaseModel):
    name: str
    description: str

class Task(TaskCreate):
    id: int

@app.get("/")
def root():
    return {"message": "Welcome to the Task Scheduler API"}

@app.post("/tasks",response_model=Task)
def create_task(task: TaskCreate):
    task_id = len(task) + 1
    new_task ={
        "id": task_id,
        "name": task.name,
        "description": task.description
    }
    task.append(new_task)
    return new_task

@app.get("/tasks",response_model=List[Task])
def get_tasks():
    return task
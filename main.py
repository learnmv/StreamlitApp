from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="My To-Do API")


#for in memory database (a simple of dicts)
fake_db = []

class ToDo(BaseModel):
    id: int
    title: str
    completed: bool

class ToDoIn(BaseModel):
    title: str
    completed:bool = False

@app.post("/todos", response_model=ToDo, status_code=201)
def create_todo(todo_in: ToDoIn):
    new_id = len(fake_db) + 1
    todo = ToDo(id=new_id, **todo_in.model_dump())
    fake_db.append(todo)
    return todo

@app.get("/todos", response_model=List[ToDo])
def get_all_todos():
    return fake_db

@app.get("/todos/{todo_id}", response_model=ToDo)
def get_todo_by_id(todo_id: int):
    for todo in fake_db:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="To-Do not found")



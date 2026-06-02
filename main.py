from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
todos: dict[int, dict] = {}
next_id = 1


class TodoCreate(BaseModel):
    title: str
    done: bool = False


@app.post("/todos")
def create_todo(todo: TodoCreate):
    global next_id
    todos[next_id] = todo.model_dump()
    created = {"id": next_id, **todos[next_id]}
    next_id += 1
    return created


@app.get("/todos")
def list_todos():
    return [{"id": k, **v} for k, v in todos.items()]


@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"id": todo_id, **todos[todo_id]}

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    del todos[todo_id]
    return {"deleted": todo_id}
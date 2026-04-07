from datetime import datetime

from fastapi import APIRouter, Body, HTTPException


router = APIRouter()


todos = [
    {
        "id": 1,
        "title": "Explain what REST means",
        "completed": False,
        "created_at": datetime.utcnow().isoformat(),
    },
    {
        "id": 2,
        "title": "Show CRUD with FastAPI",
        "completed": True,
        "created_at": datetime.utcnow().isoformat(),
    },
]
next_id = 3


@router.get("/todos")
def list_todos():
    return todos


@router.post("/todos")
def create_todo(title: str = Body(..., embed=True)):
    global next_id
    item = {
        "id": next_id,
        "title": title.strip(),
        "completed": False,
        "created_at": datetime.utcnow().isoformat(),
    }
    next_id += 1
    todos.insert(0, item)
    return item


@router.put("/todos/{todo_id}")
def update_todo(
    todo_id: int,
    title: str | None = Body(default=None, embed=True),
    completed: bool | None = Body(default=None, embed=True),
):
    for todo in todos:
        if todo["id"] == todo_id:
            if title is not None:
                todo["title"] = title.strip()
            if completed is not None:
                todo["completed"] = completed
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


@router.patch("/todos/{todo_id}/toggle")
def toggle_todo(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            todo["completed"] = not todo["completed"]
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


@router.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo["id"] == todo_id:
            removed = todos.pop(index)
            return {"deleted": True, "item": removed}
    raise HTTPException(status_code=404, detail="Todo not found")

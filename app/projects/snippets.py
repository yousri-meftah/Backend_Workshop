from datetime import datetime

from fastapi import APIRouter, Body, HTTPException


router = APIRouter()


snippets = [
    {
        "id": 1,
        "title": "GET users",
        "content": "GET /users returns a list of users.",
        "tag": "http",
        "created_at": datetime.utcnow().isoformat(),
    },
    {
        "id": 2,
        "title": "POST login",
        "content": "POST /login sends credentials in the request body.",
        "tag": "auth",
        "created_at": datetime.utcnow().isoformat(),
    },
]
next_id = 3


@router.get("/snippets")
def list_snippets():
    return snippets


@router.post("/snippets")
def create_snippet(
    name: str = Body(..., embed=True),
    body: str = Body(..., embed=True),
    label: str = Body(..., embed=True),
):
    global next_id
    snippet = {
        "id": next_id,
        "title": name.strip(),
        "content": body.strip(),
        "tag": label.strip(),
        "created_at": datetime.utcnow().isoformat(),
    }
    next_id += 1
    snippets.insert(0, snippet)
    return snippet


@router.post("/snippets/{snippet_id}")
def update_snippet(
    snippet_id: int,
    title: str | None = Body(default=None, embed=True),
    content: str | None = Body(default=None, embed=True),
    tag: str | None = Body(default=None, embed=True),
):
    for snippet in snippets:
        if snippet["id"] == snippet_id:
            if title is not None:
                snippet["title"] = title.strip()
            if content is not None:
                snippet["content"] = content.strip()
            if tag is not None:
                snippet["tag"] = tag.strip()
            return snippet
    raise HTTPException(status_code=404, detail="Snippet not found")


@router.delete("/snippets")
def delete_snippet(snippet_id: int):
    for index, snippet in enumerate(snippets):
        if snippet["id"] == snippet_id:
            removed = snippets.pop(index)
            return {"deleted": True, "item": removed}
    raise HTTPException(status_code=404, detail="Snippet not found")

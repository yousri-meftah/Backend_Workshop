from fastapi import APIRouter, Body, Cookie, Response

from app.projects.chatbot_ai import ask_gemini
from app.projects.chatbot_ai import summarize_conversation
from app.projects.chatbot_db import create_conversation_in_db
from app.projects.chatbot_db import create_user
from app.projects.chatbot_db import get_conversation_or_404
from app.projects.chatbot_db import get_conversation_for_user_or_404
from app.projects.chatbot_db import get_messages
from app.projects.chatbot_db import get_user_by_token
from app.projects.chatbot_db import list_conversations_from_db
from app.projects.chatbot_db import login_user
from app.projects.chatbot_db import save_message
from app.projects.chatbot_db import update_conversation


router = APIRouter()


@router.post("/register")
def register(
    response: Response,
    username: str = Body(..., embed=True),
    password: str = Body(..., embed=True),
):
    user = create_user(username.strip(), password.strip())
    response.set_cookie("token", user["token"], httponly=True, samesite="lax")
    return {"id": user["id"], "username": user["username"], "token": user["token"]}


@router.post("/login")
def login(
    response: Response,
    username: str = Body(..., embed=True),
    password: str = Body(..., embed=True),
):
    user = login_user(username.strip(), password.strip())
    response.set_cookie("token", user["token"], httponly=True, samesite="lax")
    return {"id": user["id"], "username": user["username"], "token": user["token"]}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("token")
    return {"logged_out": True}


@router.get("/conversations")
def list_conversations(token: str | None = Cookie(default=None)):
    user = get_user_by_token(token)
    return list_conversations_from_db(user["id"])


@router.post("/conversations")
def create_conversation(
    token: str | None = Cookie(default=None),
    title: str | None = Body(default=None, embed=True),
):
    user = get_user_by_token(token)
    return create_conversation_in_db(user["id"], title)


@router.get("/conversations/{conversation_id}")
def get_conversation(conversation_id: int, token: str | None = Cookie(default=None)):
    get_user_by_token(token)
    conversation = get_conversation_or_404(conversation_id)
    conversation["messages"] = get_messages(conversation_id)
    return conversation


@router.post("/conversations/{conversation_id}/messages")
async def send_message(
    conversation_id: int,
    token: str | None = Cookie(default=None),
    message: str = Body(..., embed=True),
    lang: str = Body(default="English", embed=True),
):
    user = get_user_by_token(token)
    conversation = get_conversation_for_user_or_404(conversation_id, user["id"])
    clean_message = message.strip()

    user_message = save_message(conversation_id, "user", clean_message)
    messages = get_messages(conversation_id)

    assistant_text = await ask_gemini(messages, lang)
    assistant_message = save_message(conversation_id, "assistant", assistant_text)
    messages = get_messages(conversation_id)

    title, summary = await summarize_conversation(messages, lang)
    if title:
        conversation["title"] = title
    elif conversation["title"].startswith("Conversation ") and clean_message:
        conversation["title"] = clean_message[:30]
    if summary:
        conversation["summary"] = summary
    update_conversation(conversation_id, conversation["title"], conversation["summary"])

    return {
        "conversation_id": conversation_id,
        "title": conversation["title"],
        "summary": conversation["summary"],
        "messages": [user_message, assistant_message],
    }

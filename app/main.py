from pathlib import Path

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from app.projects.chatbot import router as chatbot_router
from app.projects.chatbot_db import init_db as init_chatbot_db
from app.projects.quizzes import router as quizzes_router
from app.projects.snippets import router as snippets_router
from app.projects.todos import router as todos_router


BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR / "app" / "projects" / ".env")

app = FastAPI(title="Backend Workshop")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todos_router, prefix="/project1", tags=["project1"])
app.include_router(chatbot_router, prefix="/project2", tags=["project2"])
app.include_router(snippets_router, prefix="/project3", tags=["project3"])
app.include_router(quizzes_router, prefix="/project4", tags=["project4"])

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")



@app.on_event("startup")
def startup():
    init_chatbot_db()


@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/todo")
def todo_page():
    return FileResponse(STATIC_DIR / "todo.html")


@app.get("/chatbot")
def chatbot_page():
    return FileResponse(STATIC_DIR / "chatbot.html")


@app.get("/chatbot-auth")
def chatbot_auth_page():
    return FileResponse(STATIC_DIR / "chatbot-auth.html")


@app.get("/api-lab")
def api_lab_page():
    return FileResponse(STATIC_DIR / "api-lab.html")


@app.get("/quiz")
def quiz_page():
    return FileResponse(STATIC_DIR / "quiz-start.html")


@app.get("/quiz/result")
def quiz_result_page():
    return FileResponse(STATIC_DIR / "quiz-result.html")


@app.get("/quiz/{question_id}")
def quiz_question_page(question_id: int):
    return FileResponse(STATIC_DIR / "quiz-question.html")

import secrets
import sqlite3
from datetime import datetime
from pathlib import Path

from fastapi import HTTPException


DB_PATH = Path(__file__).resolve().parents[2] / "chatbot.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            token TEXT
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT NOT NULL,
            summary TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (conversation_id) REFERENCES conversations (id)
        )
        """
    )

    columns = [row[1] for row in cursor.execute("PRAGMA table_info(conversations)").fetchall()]
    if "user_id" not in columns:
        cursor.execute("ALTER TABLE conversations ADD COLUMN user_id INTEGER")

    count = cursor.execute("SELECT COUNT(*) FROM conversations").fetchone()[0]
    if count == 0:
        created_at = datetime.utcnow().isoformat()
        cursor.execute(
            "INSERT INTO conversations (user_id, title, summary, created_at) VALUES (?, ?, ?, ?)",
            (None, "Backend Basics", "Simple seeded conversation for the workshop.", created_at),
        )
        conversation_id = cursor.lastrowid
        cursor.execute(
            "INSERT INTO messages (conversation_id, role, content, created_at) VALUES (?, ?, ?, ?)",
            (
                conversation_id,
                "assistant",
                "Ask me anything about APIs. This route can now call Gemini if GEMINI_API_KEY is set.",
                created_at,
            ),
        )

    connection.commit()
    connection.close()


def create_user(username: str, password: str):
    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password are required")
    token = secrets.token_hex(24)
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, token) VALUES (?, ?, ?)",
            (username, password, token),
        )
        user_id = cursor.lastrowid
        connection.commit()
    except sqlite3.IntegrityError:
        connection.close()
        raise HTTPException(status_code=400, detail="Username already exists")
    connection.close()
    return {"id": user_id, "username": username, "token": token}


def login_user(username: str, password: str):
    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password are required")
    token = secrets.token_hex(24)
    connection = get_connection()
    user = connection.execute(
        "SELECT id, username FROM users WHERE username = ? AND password = ?",
        (username, password),
    ).fetchone()
    if not user:
        connection.close()
        raise HTTPException(status_code=401, detail="Invalid username or password")
    connection.execute("UPDATE users SET token = ? WHERE id = ?", (token, user["id"]))
    connection.commit()
    connection.close()
    return {"id": user["id"], "username": user["username"], "token": token}


def get_user_by_token(token: str | None):
    if not token:
        raise HTTPException(status_code=401, detail="Login required")
    connection = get_connection()
    user = connection.execute(
        "SELECT id, username, token FROM users WHERE token = ?",
        (token,),
    ).fetchone()
    connection.close()
    if not user:
        raise HTTPException(status_code=401, detail="Login required")
    return dict(user)


def list_conversations_from_db(user_id: int):
    connection = get_connection()
    rows = connection.execute(
        """
        SELECT
            conversations.id,
            conversations.title,
            conversations.summary,
            conversations.created_at,
            COUNT(messages.id) AS message_count
        FROM conversations
        LEFT JOIN messages ON messages.conversation_id = conversations.id
        WHERE conversations.user_id = ?
        GROUP BY conversations.id
        ORDER BY conversations.id DESC
        """,
        (user_id,),
    ).fetchall()
    connection.close()
    return [dict(row) for row in rows]


def create_conversation_in_db(user_id: int, title: str | None):
    created_at = datetime.utcnow().isoformat()
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO conversations (user_id, title, summary, created_at) VALUES (?, ?, ?, ?)",
        (user_id, title or "New conversation", "No summary yet.", created_at),
    )
    conversation_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return {
        "id": conversation_id,
        "title": title or "New conversation",
        "summary": "No summary yet.",
        "created_at": created_at,
        "messages": [],
    }


def get_conversation_or_404(conversation_id: int):
    connection = get_connection()
    conversation = connection.execute(
        "SELECT id, user_id, title, summary, created_at FROM conversations WHERE id = ?",
        (conversation_id,),
    ).fetchone()
    connection.close()
    if conversation:
        return dict(conversation)
    raise HTTPException(status_code=404, detail="Conversation not found")


def get_conversation_for_user_or_404(conversation_id: int, user_id: int):
    connection = get_connection()
    conversation = connection.execute(
        """
        SELECT id, user_id, title, summary, created_at
        FROM conversations
        WHERE id = ? AND user_id = ?
        """,
        (conversation_id, user_id),
    ).fetchone()
    connection.close()
    if conversation:
        return dict(conversation)
    raise HTTPException(status_code=404, detail="Conversation not found")


def get_messages(conversation_id: int):
    connection = get_connection()
    rows = connection.execute(
        """
        SELECT role, content, created_at
        FROM messages
        WHERE conversation_id = ?
        ORDER BY id
        """,
        (conversation_id,),
    ).fetchall()
    connection.close()
    return [dict(row) for row in rows]


def save_message(conversation_id: int, role: str, content: str):
    created_at = datetime.utcnow().isoformat()
    connection = get_connection()
    connection.execute(
        """
        INSERT INTO messages (conversation_id, role, content, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (conversation_id, role, content, created_at),
    )
    connection.commit()
    connection.close()
    return {
        "role": role,
        "content": content,
        "created_at": created_at,
    }


def update_conversation(conversation_id: int, title: str, summary: str):
    connection = get_connection()
    connection.execute(
        "UPDATE conversations SET title = ?, summary = ? WHERE id = ?",
        (title, summary, conversation_id),
    )
    connection.commit()
    connection.close()

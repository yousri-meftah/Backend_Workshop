import os

import anyio
from fastapi import HTTPException
import google.genai as genai


def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY is missing",
        )
    return genai.Client(api_key=api_key)


def build_chat_prompt(messages: list[dict], lang: str):
    lines = [
        "You are a helpful assistant for a backend workshop.",
        f"Reply in {lang}.",
        "Conversation:",
    ]
    for message in messages:
        lines.append(f"{message['role']}: {message['content']}")
    return "\n".join(lines)


def build_summary_prompt(messages: list[dict], lang: str):
    lines = [
        "Read this conversation and answer with exactly two lines.",
        f"Use {lang}.",
        "Line 1 must start with: Title:",
        "Line 2 must start with: Summary:",
        "Keep both short.",
        "",
    ]
    for message in messages:
        lines.append(f"{message['role']}: {message['content']}")
    return "\n".join(lines)


def generate_text(prompt: str):
    client = get_gemini_client()
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    response = client.models.generate_content(model=model, contents=prompt)
    return (response.text or "").strip()


async def ask_gemini(messages: list[dict], lang: str):
    prompt = build_chat_prompt(messages, lang)
    return await anyio.to_thread.run_sync(generate_text, prompt)


async def summarize_conversation(messages: list[dict], lang: str):
    prompt = build_summary_prompt(messages, lang)
    text = await anyio.to_thread.run_sync(generate_text, prompt)
    title = ""
    summary = ""

    for line in text.splitlines():
        if line.lower().startswith("title:"):
            title = line.split(":", 1)[1].strip()
        if line.lower().startswith("summary:"):
            summary = line.split(":", 1)[1].strip()

    return title, summary

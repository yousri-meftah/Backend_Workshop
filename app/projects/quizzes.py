from fastapi import APIRouter

from app.projects.quiz_seed import get_quiz_question_by_position_or_404
from app.projects.quiz_seed import get_quiz_session_or_404


router = APIRouter()


@router.get("/sessions/{session_id}")
def get_session(session_id: int):
    return get_quiz_session_or_404(session_id)


@router.get("/sessions/{session_id}/quiz/{question_position}")
def get_question_by_position(session_id: int, question_position: int):
    return get_quiz_question_by_position_or_404(session_id, question_position)

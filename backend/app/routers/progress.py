from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session

from services.auth import require_user
from database import (
    get_db, User,
    list_attempts_for_user,
    get_question_by_id,
    get_user_accuracy,
)

router = APIRouter(prefix="/api", tags=["practice"])

class AttemptRecord(BaseModel):
    question_id: int
    user_answer: str
    correct: bool
    submitted_at: str 

class ProgressResponse(BaseModel):
    attempts: List[AttemptRecord]
    accuracy: float

@router.get("/progress", response_model=ProgressResponse)
def get_user_progress(limit: int = 20, db: Session = Depends(get_db), current_user: User = Depends(require_user)):
    attempts = list_attempts_for_user(db, user_id=current_user.id, limit=limit)
    accuracy = get_user_accuracy(db, user_id=current_user.id)
    attempt_records = [
        AttemptRecord(
            question_id=attempt.question_id,
            user_answer=attempt.user_answer,
            correct=attempt.correct,
            submitted_at=attempt.submitted_at.isoformat(),
        )
        for attempt in attempts
    ]

    return ProgressResponse(attempts=attempt_records, accuracy=accuracy)


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.auth import require_user
from models import AttemptRequest, AttemptResponse
from services.grading import grade_answer
from database import get_db, Question, get_question_by_id, record_attempt

router = APIRouter(prefix="/api", tags=["attempts"])

# I might change this so that attempts do not require authentication
# For now I keep it so that it wires into the progress tracking
# Removing might be adding a check in progress tracking instead and
# allowing unauthenticated users to submit attempts without persistence
@router.post("/attempts", response_model=AttemptResponse)
def submit_attempt(payload: AttemptRequest, db: Session = Depends(get_db), current_user = Depends(require_user)):
    question = get_question_by_id(db, payload.question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    is_correct = grade_answer(payload.user_answer, question.solution or "")
    feedback = None
    record_attempt(
        db,
        user_id=current_user.id,
        question_id=question.id,
        user_answer=payload.user_answer,
        correct=is_correct,
    )


    return AttemptResponse(correct=is_correct, feedback=feedback)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import AttemptRequest, AttemptResponse
from services.grading import grade_answer
from database import get_db, Question

router = APIRouter(prefix="/api", tags=["attempts"])

@router.post("/attempts", response_model=AttemptResponse)
def submit_attempt(payload: AttemptRequest, db: Session = Depends(get_db)):
    question = db.query(Question).get(payload.question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    is_correct = grade_answer(payload.user_answer, question.solution or "")
    feedback = None
    # (Optional) choose whether to reveal anything on submit; keeping it minimal now.
    # feedback = "Nice job!" if is_correct else "Try again."

    return {"correct": is_correct, "feedback": feedback}

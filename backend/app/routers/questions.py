from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, Question, get_question_by_id
from models import QuestionDetail, QuestionListItem

router = APIRouter(prefix="/api", tags=["questions"])

@router.get("/questions", response_model=list[QuestionListItem])
# might move this method to the database.py file later
def list_questions(topic_id: int | None = None, db: Session = Depends(get_db)):
    q = db.query(Question)
    if topic_id is not None:
        q = q.filter(Question.topic_id == topic_id)
    rows = q.all()
    return [
        {
            "id": r.id,
            "topic_id": r.topic_id,
            "difficulty": r.difficulty,
            "question": r.text,
        }
        for r in rows
    ]

@router.get("/questions/{question_id}", response_model=QuestionDetail)
def get_question_by_id_route(question_id: int, db: Session = Depends(get_db)):
    question = get_question_by_id(db, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return {
        "id": question.id,
        "topic_id": question.topic_id,
        "difficulty": question.difficulty,
        "question": question.text,
    }
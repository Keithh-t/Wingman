from pydantic import BaseModel

class QuestionListItem(BaseModel):
    id: int
    topic_id: int
    difficulty: int
    question: str

class QuestionDetail(QuestionListItem):
    pass

class AttemptRequest(BaseModel):
    question_id: int
    user_answer: str

class AttemptResponse(BaseModel):
    correct: bool
    feedback: str | None = None
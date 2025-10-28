from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from database import get_db, list_question, list_topics
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
        allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")   
async def read_root():
    return {"Hello": "World"}

@app.get("/api/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/api/topics")
def api_list_topics(db: Session = Depends(get_db)):
    topics = list_topics(db)
    return [{"id": t.id, "slug": t.slug, "name": t.name} for t in topics]

@app.get("/api/questions")
def api_list_question(
    topic_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    questions = list_question(db, topic_id=topic_id)
    return [{"id": q.id,
            "question": q.text,
            "answer": q.solution,
            "topic_id": q.topic_id
            } for q in questions]
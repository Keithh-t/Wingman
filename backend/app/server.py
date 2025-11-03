from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from routers import attempts, questions, auth_routes, progress

from database import get_db, list_topics, Question
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

app.include_router(questions.router)
app.include_router(attempts.router)
app.include_router(auth_routes.router)
app.include_router(progress.router)
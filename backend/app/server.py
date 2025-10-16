from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

# Temporary in-memory data so the frontend can work now
_FAKE_TOPICS = [
    {"id": 1, "slug": "controls", "name": "Controls"},
    {"id": 2, "slug": "fluids", "name": "Fluids"},
]

@app.get("/api/topics")
def list_topics():
    return _FAKE_TOPICS
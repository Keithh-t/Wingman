# createdatabase.py
from sqlalchemy import select
from app.database import (
    engine, SessionLocal, Base,
    Topic, Question, User, Attempt  # <-- import new models so they're registered
)

def create_and_seed():
    # Create ALL tables known to Base (users, attempts, topics, questions)
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        # ---- Idempotent topic seed (by slug) ----
        slug_to_name = {
            "mathematics": "Mathematics",
            "science": "Science",
            "history": "History",
        }

        # fetch existing slugs
        existing = {t.slug for t in db.scalars(select(Topic)).all()}

        # create any missing topics
        new_topics = [
            Topic(name=name, slug=slug)
            for slug, name in slug_to_name.items()
            if slug not in existing
        ]
        if new_topics:
            db.add_all(new_topics)
            db.flush()  # assigns IDs

        # build a map of slug -> id (covers both existing and newly inserted)
        topics = {t.slug: t.id for t in db.scalars(select(Topic)).all()}

        # ---- Idempotent question seed (by exact text) ----
        # Only add a few sample questions if they don't already exist (by text)
        existing_q_texts = {q.text for q in db.scalars(select(Question)).all()}

        seed_questions = [
            ("mathematics", "What is 2 + 2?", 1, "4"),
            ("mathematics", "Derivative of x^2?", 2, "2x"),
            ("science",     "What is H2O?", 1, "Water"),
            ("history",     "First US president?", 1, "George Washington"),
        ]

        new_qs = []
        for slug, text, diff, sol in seed_questions:
            if text in existing_q_texts:
                continue
            topic_id = topics.get(slug)
            if topic_id:
                new_qs.append(Question(topic_id=topic_id, text=text, difficulty=diff, solution=sol))

        if new_qs:
            db.add_all(new_qs)

        db.commit()

if __name__ == "__main__":
    create_and_seed()
    print("Tables ensured and seed completed safely.")

# createdatabase.py
from sqlalchemy import select
from app.database import (
    engine, SessionLocal, Base,
    Topic, Question, User, Attempt  # ensure models are registered
)

# ai populated
def create_and_seed():
    # Create all tables
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        # ---- Topics (idempotent by slug) ----
        slug_to_name = {
            "statics": "Statics",
            "beam_theory": "Beam Theory",
            "buckling_and_stability": "Buckling & Stability",
            "mechanics_of_materials": "Mechanics of Materials",
            "fatigue_and_failure": "Fatigue & Failure",
            "materials_engineering": "Materials Engineering",
        }

        existing_slugs = {t.slug for t in db.scalars(select(Topic)).all()}
        new_topics = [
            Topic(name=name, slug=slug)
            for slug, name in slug_to_name.items()
            if slug not in existing_slugs
        ]
        if new_topics:
            db.add_all(new_topics)
            db.flush()  # assign IDs

        # Map slug -> id (covers both existing and newly inserted)
        topics = {t.slug: t.id for t in db.scalars(select(Topic)).all()}

        # ---- Questions (idempotent by exact text) ----
        # NOTE: Questions are chosen to have single, canonical answers (numbers/short words).
        # Units are specified in the prompt; answers are numeric strings or single words.
        seed_questions = [
            # BEAM THEORY
            (
                "beam_theory",
                "Cantilever deflection: A point load F=50 N is applied at the free end of a cantilever of length L=2.0 m with E=200 GPa and I=2×10^-6 m^4. "
                "Using δ = (F L^3)/(3 E I), give the deflection in mm to 3 d.p.",
                2,
                "0.333"  # mm
            ),
            (
                "beam_theory",
                "Simply supported beam with UDL: For w=200 N/m and L=3.0 m, compute the maximum bending moment M_max = w L^2 / 8 (units: N·m).",
                1,
                "225"
            ),
            (
                "beam_theory",
                "Fixed-end moment: A cantilever of length L=0.5 m carries a tip load P=100 N. Give the fixed-end moment M = P·L (units: N·m).",
                1,
                "50"
            ),
            (
                "beam_theory",
                "Second moment of area (rectangle): For b=50 mm, h=100 mm, compute I = (1/12) b h^3 (units: mm^4).",
                1,
                "4166667"
            ),
            (
                "beam_theory",
                "Scaling: For a cantilever with tip load, if the length L is halved, by what factor does δ = (F L^3)/(3 E I) change? (answer as a fraction like 1/8)",
                1,
                "1/8"
            ),

            # STATICS
            (
                "statics",
                "UDL reactions: A simply supported beam (length L=4 m) with w=1.2 kN/m across the span. What is reaction at A, R_A = (w·L)/2 (units: kN)?",
                1,
                "2.4"
            ),

            # BUCKLING & STABILITY
            (
                "buckling_and_stability",
                "Euler buckling (pinned–pinned): For E=70 GPa, I=5×10^-6 m^4, L=1.0 m, K=1.0, compute P_cr = (π^2 E I)/(K L)^2 in MN (to 2 d.p.).",
                2,
                "3.45"
            ),

            # MECHANICS OF MATERIALS
            (
                "mechanics_of_materials",
                "Hooke’s law: Aluminum with E=70 GPa is strained by ε=0.002. Compute σ = E·ε in MPa.",
                1,
                "140"
            ),
            (
                "mechanics_of_materials",
                "Axial stress: A 10 mm diameter rod carries F=20 kN in tension. Give σ = F/A in MPa (to 1 d.p.).",
                2,
                "254.6"
            ),
            (
                "mechanics_of_materials",
                "Bending stress: For M=225 N·m on a rectangular section b=40 mm, h=80 mm, compute σ = M c / I (MPa, to 2 d.p.).",
                2,
                "5.27"
            ),
            (
                "mechanics_of_materials",
                "Factor of Safety: If a bar with UTS=400 MPa sees a working stress of 200 MPa, give FOS = UTS / WorkingStress.",
                1,
                "2"
            ),

            # FATIGUE & FAILURE
            (
                "fatigue_and_failure",
                "Miner’s Rule: Given cycles at three stress levels produce N/Nf of 1e6/2e6, 5e5/1e6, and 1e5/2.5e5, compute total damage D (to 1 d.p.).",
                2,
                "1.4"
            ),

            # MATERIALS ENGINEERING (short canonical word)
            (
                "materials_engineering",
                "Neutral axis location: For a symmetric rectangular cross-section in pure bending, where is the neutral axis? (one word)",
                1,
                "centroid"
            ),
        ]

        existing_q_texts = {q.text for q in db.scalars(select(Question)).all()}
        new_qs = []
        for slug, text, diff, sol in seed_questions:
            if text in existing_q_texts:
                continue
            topic_id = topics.get(slug)
            if not topic_id:
                # Skip if topic wasn't created (shouldn't happen if slugs above are intact)
                continue
            new_qs.append(
                Question(topic_id=topic_id, text=text, difficulty=diff, solution=str(sol))
            )

        if new_qs:
            db.add_all(new_qs)

        db.commit()

if __name__ == "__main__":
    create_and_seed()
    print("Tables ensured and seed completed safely.")

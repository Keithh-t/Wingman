# Not wired yet—this is just a parking spot for when your DB is ready.

DATABASE_URL = "postgresql+psycopg://<user>:<password>@<host>:5432/wingman?sslmode=require"

# Example of what you'll add later:
# from sqlalchemy import create_engine
# engine = create_engine(DATABASE_URL, pool_pre_ping=True)
# from sqlalchemy.orm import sessionmaker
# SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

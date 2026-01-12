import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import URL

# 1️⃣ Read DATABASE_URL from environment if present
DATABASE_URL = os.getenv("DATABASE_URL")

# 2️⃣ Fallback for local development
if not DATABASE_URL:
    DATABASE_URL = URL.create(
        drivername="postgresql+psycopg2",
        username="postgres",
        password="Farhan@2004",   # OK for local dev
        host="localhost",
        port=5432,
        database="enterprise_db"
    )

print("DATABASE_URL =", DATABASE_URL)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


from os import getenv

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

load_dotenv()
POSTGRES_DB = getenv("POSTGRES_DB")
POSTGRES_USER = getenv("POSTGRES_USER")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD")

DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}"
)

engine = create_engine(DATABASE_URL)
session_factory = sessionmaker(bind=engine)
SessionLocal = scoped_session(session_factory)

Base = declarative_base()


def test_connection():
    try:
        with SessionLocal() as session:
            result = session.execute(text("SELECT 1"))
            return True, result.scalar()
    except OperationalError as e:
        return False, str(e)


if __name__ == "__main__":
    success, output = test_connection()
    if success:
        print("Connection successful. DB responded with:", output)
    else:
        print("Connection failed:", output)

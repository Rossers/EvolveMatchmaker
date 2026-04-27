import os
import time

from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")


MAX_DB_RETRIES = 10
DB_RETRY_DELAY_SECONDS = 2


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def wait_for_database() -> None:
    for attempt in range(1, MAX_DB_RETRIES + 1):
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            print("Database connection successful")
            return

        except Exception as error:
            print(
                f"Database not ready yet "
                f"(attempt {attempt}/{MAX_DB_RETRIES}): {error}"
            )
            time.sleep(DB_RETRY_DELAY_SECONDS)

    raise RuntimeError("Could not connect to database")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.database import SessionLocal

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @app.get("/session")
# def get_session(session: Annotated[Session, Depends(get_db)]):
#     test = session.execute(text("SELECT 1"))
#     return {"db": test.scalar()}


from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import mapped_column
from app.core.database import Base

class BaseAbstract(Base):
    __abstract__ = True
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(30), nullable=False, index=True)
    created_at = mapped_column(DateTime, nullable=False, index=True)

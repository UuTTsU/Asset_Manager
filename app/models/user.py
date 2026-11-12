from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column

from app.core.database import Base
from .baseAbstract import BaseAbstract
class User(BaseAbstract):
    __tablename__ = "users"
    last_name = mapped_column(String(20), index=True)
    email = mapped_column(String(50), unique=True, index=True, nullable=False)
    first_name = mapped_column(String(30), index=True, nullable=False)
    password = mapped_column(String(100), index=True)
    birthday = mapped_column(DateTime, index=True)

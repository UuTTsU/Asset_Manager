from sqlalchemy import String, Date
from sqlalchemy.orm import mapped_column

from app.core.database import Base
from .baseAbstract import BaseAbstract
class User(BaseAbstract):
    __tablename__ = "users"
    last_name = mapped_column(String(20), index=True)
    email = mapped_column(String(50), unique=True, index=True, nullable=False)
    password = mapped_column(String(255), index=True, nullable=False)
    birthday = mapped_column(Date, index=True, nullable=False)

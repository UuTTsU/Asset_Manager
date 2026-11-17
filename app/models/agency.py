from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column
from .baseAbstract import BaseAbstract

class Agency(BaseAbstract):
    __tablename__ = 'agencies'
    name = mapped_column(String(30), nullable=False, index=True)
    user_id = mapped_column(Integer, ForeignKey('users.id', ondelete="CASCADE"), index=True)

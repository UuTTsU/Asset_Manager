from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import mapped_column
from .baseAbstract import BaseAbstract

class Agency(BaseAbstract):
    __tablename__ = 'agencies'
    user_id = mapped_column(Integer, ForeignKey('users.id', ondelete="CASCADE"), index=True)

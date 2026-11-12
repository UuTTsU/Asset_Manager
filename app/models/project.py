from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column
from .baseAbstract import BaseAbstract

class Project(BaseAbstract):
    __tablename__ = 'projects'
    agency_id = mapped_column(Integer, ForeignKey('agencies.id', ondelete="CASCADE"), index=True)
    description = mapped_column(String(50), nullable=False, index=True)
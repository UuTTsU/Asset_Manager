from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import mapped_column
from .baseAbstract import BaseAbstract

class Project(BaseAbstract):
    __tablename__ = 'projects'
    agency_id = mapped_column(Integer, ForeignKey('agency.id'), primary_key=True, on_delete='cascade')
    description = mapped_column(Text(50), nullable=False)
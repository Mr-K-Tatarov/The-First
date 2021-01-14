from sqlalchemy import Column, VARCHAR

from db.models.base import BaseModel


class DBEmployee(BaseModel):

    __tablename__ = 'employee'

    first_name = Column(VARCHAR(50))
    last_name = Column(VARCHAR(50))


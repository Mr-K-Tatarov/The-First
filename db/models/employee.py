from sqlalchemy import Column, VARCHAR, VARBINARY, BOOLEAN

from db.models.base import BaseModel


class DBEmployee(BaseModel):

    __tablename__ = 'employee'

    login = Column(VARCHAR(20), unique=True, nullable=False)
    password = Column(VARBINARY(), nullable=False)
    first_name = Column(VARCHAR(50))
    last_name = Column(VARCHAR(50))
    is_delete = Column(BOOLEAN(), nullable=False, default=False)
    position = Column(VARCHAR(50))
    department = Column(VARCHAR(50))

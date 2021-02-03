from sqlalchemy import Column, VARCHAR, Integer

from db.models.base import BaseModel


class DBMessage(BaseModel):
    __tablename__ = "message"

    message = Column(VARCHAR(255), nullable=False)
    sender_id = Column(Integer, nullable=False)
    recipient_id = Column(Integer, nullable=False)

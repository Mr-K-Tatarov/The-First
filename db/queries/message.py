from typing import List

from api.request import RequestUpdateMessageDto
from db.database import DBSession
from db.exceptions import DBMessageNotExists
from db.models import DBMessage


def create_message(
        session: DBSession, *, message: str, sender_id: str, recipient_id: str
) -> DBMessage:
    new_message = DBMessage(
        message=message,
        sender_id=sender_id,
        recipient_id=recipient_id,
    )
    session.add_model(new_message)

    return new_message


def get_message_by_id(session: DBSession, *, message_id: int) -> DBMessage:
    db_message = session.query(DBMessage).filter(DBMessage.id == message_id).first()
    if db_message is None:
        raise DBMessageNotExists

    return db_message


def get_messages_by_recipient_id(
        session: DBSession, *, recipient_id: int
) -> List[DBMessage]:
    db_messages = (
            session.query(DBMessage).filter(DBMessage.recipient_id == recipient_id).all() or []
    )

    return db_messages


def update_message(
        session: DBSession, *, message: RequestUpdateMessageDto, message_id: int
) -> DBMessage:
    db_message = get_message_by_id(session, message_id=message_id)

    for attr in message.fields:
        if hasattr(message, attr):
            value = getattr(message, attr)
            setattr(db_message, attr, value)

    return db_message


def delete_message(session: DBSession, message_id: int) -> DBMessage:
    db_message = get_message_by_id(session, message_id=message_id)
    session.delete_model(db_message)
    return db_message

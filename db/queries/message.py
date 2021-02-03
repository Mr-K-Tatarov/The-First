from db.database import DBSession
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

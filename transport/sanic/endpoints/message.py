from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request import RequestCreateMessageDto
from api.response import ResponseMessageDto
from db.database import DBSession
from db.exceptions import DBUserNotExists, DBIntegrityException, DBDataException
from db.queries.message import create_message
from db.queries.user import get_user_by_login
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicUserNotFound, SanicDBException


class CreateMessageEndpoint(BaseEndpoint):
    async def method_post(
            self,
            request: Request,
            body: dict,
            session: DBSession,
            user_id: int,
            *args,
            **kwargs
    ) -> BaseHTTPResponse:
        request_model = RequestCreateMessageDto(body)

        try:
            recipient = get_user_by_login(session, login=request_model.recipient)
        except DBUserNotExists:
            raise SanicUserNotFound("Recipient not found")

        db_message = create_message(
            session,
            message=request_model.message,
            recipient_id=recipient.id,
            sender_id=body["user_id"],
        )
        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseMessageDto(db_message)

        return await self.make_response_json(status=200, body=response_model.dump())

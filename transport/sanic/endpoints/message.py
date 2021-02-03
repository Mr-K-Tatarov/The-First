from sanic.exceptions import NotFound, Unauthorized
from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request import RequestCreateMessageDto, RequestUpdateMessageDto
from api.response import ResponseMessageDto
from db.database import DBSession
from db.exceptions import (
    DBUserNotExists,
    DBIntegrityException,
    DBDataException,
    DBMessageNotExists,
)
from db.queries.message import (
    create_message,
    update_message,
    delete_message,
    get_message_by_id, get_messages_by_recipient_id,
)
from db.queries.user import get_user_by_login
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicUserNotFound, SanicDBException


class MessagesEndpoint(BaseEndpoint):
    async def method_get(
            self,
            request: Request,
            body: dict,
            session: DBSession,
            *args,
            **kwargs,
    ) -> BaseHTTPResponse:
        """
        Get messages for me
        :param request:
        :param body:
        :param session:
        :param args:
        :param kwargs:
        :return:
        """
        my_user_id = int(body["sub"])
        db_messages = get_messages_by_recipient_id(session, recipient_id=my_user_id)

        messages = ResponseMessageDto(db_messages, many=True).dump()

        return await self.make_response_json(status=200, body={"messages": messages})

    async def method_post(
            self,
            request: Request,
            body: dict,
            session: DBSession,
            *args,
            **kwargs,
    ) -> BaseHTTPResponse:
        """
        Send message to recipient by login
        :param request:
        :param body:
        :param session:
        :param args:
        :param kwargs:
        :return:
        """
        request_model = RequestCreateMessageDto(body)

        try:
            recipient = get_user_by_login(session, login=request_model.recipient)
        except DBUserNotExists as e:
            raise SanicUserNotFound(f"Recipient {request_model.recipient} not found") from e

        db_message = create_message(
            session,
            message=request_model.message,
            recipient_id=recipient.id,
            sender_id=body["sub"],
        )
        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseMessageDto(db_message)

        return await self.make_response_json(status=200, body=response_model.dump())


class MessageByIdEndpoint(BaseEndpoint):
    async def method_get(
            self,
            request: Request,
            body: dict,
            session: DBSession,
            message_id: int,
            *args,
            **kwargs,
    ) -> BaseHTTPResponse:
        """
        Get message by id
        :param request:
        :param body:
        :param session:
        :param message_id:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            db_message = get_message_by_id(session, message_id=message_id)
        except DBMessageNotExists as e:
            raise NotFound(f"Message {message_id} not found") from e

        if body["sub"] not in (db_message.sender_id, db_message.recipient_id):
            raise Unauthorized("user is not recipient or sender")

        response_model = ResponseMessageDto(db_message)

        return await self.make_response_json(status=200, body=response_model.dump())

    async def method_patch(
            self,
            request: Request,
            body: dict,
            session: DBSession,
            message_id: int,
            *args,
            **kwargs,
    ) -> BaseHTTPResponse:
        """
        Update message by id
        :param request:
        :param body:
        :param session:
        :param message_id:
        :param args:
        :param kwargs:
        :return:
        """
        request_model = RequestUpdateMessageDto(body)

        try:
            db_message = update_message(
                session, message=request_model, message_id=message_id
            )
        except DBMessageNotExists as e:
            raise NotFound(f"Message {message_id} not found") from e

        if body["sub"] != db_message.sender_id:
            raise Unauthorized("user is not sender")

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseMessageDto(db_message)

        return await self.make_response_json(status=200, body=response_model.dump())

    async def method_delete(
            self,
            request: Request,
            body: dict,
            session: DBSession,
            message_id: int,
            *args,
            **kwargs,
    ) -> BaseHTTPResponse:
        """
        Delete message by id
        :param request:
        :param body:
        :param session:
        :param message_id:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            db_message = delete_message(session, message_id=message_id)
        except DBMessageNotExists as e:
            raise NotFound(f"Message {message_id} not found") from e

        if body["sub"] not in (db_message.sender_id, db_message.recipient_id):
            raise Unauthorized("user is not recipient or sender")

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        return await self.make_response_json(status=204)

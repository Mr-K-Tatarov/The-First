from sanic.exceptions import Unauthorized
from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request import RequestPatchUserDto
from api.response import ResponseUserDto
from db.database import DBSession
from db.exceptions import DBUserNotExists, DBDataException, DBIntegrityException
from db.queries.user import update_user, delete_user, get_user_by_id
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicUserNotFound, SanicDBException


class UserEndpoint(BaseEndpoint):
    async def method_patch(
            self,
            request: Request,
            body: dict,
            session: DBSession,
            user_id: int,
            *args,
            **kwargs
    ) -> BaseHTTPResponse:
        if user_id != body["sub"]:
            raise Unauthorized("user can update only himself")

        request_model = RequestPatchUserDto(body)

        try:
            db_user = update_user(session, request_model, user_id)
        except DBUserNotExists:
            raise SanicUserNotFound("User not found")

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseUserDto(db_user)

        return await self.make_response_json(status=200, body=response_model.dump())

    async def method_delete(
            self,
            request: Request,
            body: dict,
            session: DBSession,
            user_id: int,
            *args,
            **kwargs
    ) -> BaseHTTPResponse:
        if user_id != body["sub"]:
            raise Unauthorized("user can delete only himself")

        try:
            _ = delete_user(session, user_id)
        except DBUserNotExists:
            raise SanicUserNotFound("User not found")

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        return await self.make_response_json(status=204)

    async def method_get(
            self,
            request: Request,
            body: dict,
            session: DBSession,
            user_id: int,
            *args,
            **kwargs
    ) -> BaseHTTPResponse:
        if user_id != body["sub"]:
            raise Unauthorized("user can get only himself")

        try:
            db_user = get_user_by_id(session, user_id=user_id)
        except DBUserNotExists:
            raise SanicUserNotFound("User not found")

        response_model = ResponseUserDto(db_user)

        return await self.make_response_json(body=response_model.dump(), status=200)

from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request import RequestPatchUserDto
from api.response import ResponseUserDto
from db.database import DBSession
from db.exceptions import DBUserNotExists, DBDataException, DBIntegrityException
from db.queries.user import update_user, delete_user, get_user_by_id
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicUserNotFound, SanicDBException


class CreateMessageEndpoint(BaseEndpoint):

    async def method_post(
            self, request: Request, body: dict, session: DBSession, user_id: int, *args, **kwargs
    ) -> BaseHTTPResponse:

        request_model = RequestPatchUserDto(body)

        try:
            db_user = update_user(session, request_model, user_id)
        except DBUserNotExists:
            raise SanicUserNotFound('User not found')

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseUserDto(db_user)

        return await self.make_response_json(status=200, body=response_model.dump())
from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.response.auth_user import ResponseAuthUserDto, AuthResponseObject
from db.queries.user import get_user_by_login
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicUserNotFound, SanicPasswordHashException

from api.request import RequestAuthUserDto

from db.exceptions import DBUserNotExists

from helpers.password import check_hash, CheckPasswordHashException

from helpers.auth import create_token


class AuthEndpoint(BaseEndpoint):

    async def method_post(self, request: Request, body: dict, session, *args, **kwargs) -> BaseHTTPResponse:

        request_model = RequestAuthUserDto(body)

        try:
            db_user = get_user_by_login(session, login=request_model.login)
        except DBUserNotExists:
            raise SanicUserNotFound('User not found')

        try:
            check_hash(request_model.password, db_user.password)
        except CheckPasswordHashException:
            raise SanicPasswordHashException('Wrong password')

        payload = {
            'user_id': db_user.id,
        }
        token = create_token(payload)
        response = AuthResponseObject(token)

        response_model = ResponseAuthUserDto(response)

        return await self.make_response_json(
            body=response_model.dump(),
            status=200,
        )

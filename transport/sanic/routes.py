from typing import Tuple

from configs.config import ApplicationConfig
from context import Context
from transport.sanic import endpoints


def get_routes(config: ApplicationConfig, context: Context) -> Tuple:
    return (
        endpoints.HealthEndpoint(
            config=config, context=context, uri='/', methods=('GET', 'POST'),
        ),
        endpoints.CreateUserEndpoint(
            config, context, uri='/user', methods=['POST'],
        ),
        endpoints.UserEndpoint(
            config, context, uri='/user/<user_id:int>', methods=['GET', 'PATCH', 'DELETE'], auth_required=True,
        ),
        endpoints.AuthEndpoint(
            config, context, uri='/auth', methods=['POST'],
        ),
        endpoints.CreateMessageEndpoint(
            config, context, uri='/msg', methods=['POST'],
        ),



    )

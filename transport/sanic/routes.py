from typing import Tuple

from configs.config import ApplicationConfig
from context import Context
from transport.sanic import endpoints


def get_routes(config: ApplicationConfig, context: Context) -> Tuple:
    return (
        endpoints.HealthEndpoint(
            config=config,
            context=context,
            uri="/",
            methods=("GET", "POST"),
        ),
        endpoints.CreateUserEndpoint(
            config,
            context,
            uri="/user",
            methods=["POST"],
        ),
        endpoints.UserEndpoint(
            config,
            context,
            uri="/user/<user_id:int>",
            methods=["GET", "PATCH", "DELETE"],
            auth_required=True,
        ),
        endpoints.AuthEndpoint(
            config,
            context,
            uri="/auth",
            methods=["POST"],
        ),
        endpoints.MessagesEndpoint(
            config,
            context,
            uri="/msg",
            methods=["POST", "GET"],
            auth_required=True,
        ),
        endpoints.MessageByIdEndpoint(
            config,
            context,
            uri="/msg/<message_id:int>",
            methods=["GET", "PATCH", "DELETE"],
            auth_required=True,
        ),
    )

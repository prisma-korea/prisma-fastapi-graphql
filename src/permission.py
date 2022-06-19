import typing
from fastapi import Request, WebSocket
from strawberry.permission import BasePermission
from strawberry.types import Info

from src.utils.auth import decodeJWT


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        request: typing.Union[Request, WebSocket] = info.context["request"]
        authorization = request.headers.get("Authorization")

        if "Authorization" in request.headers:
            auth = decodeJWT(authorization)
            return auth

        return False

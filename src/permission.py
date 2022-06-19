import os
import typing
import jwt
from fastapi import Request, WebSocket
from strawberry.permission import BasePermission
from strawberry.types import Info


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        request: typing.Union[Request, WebSocket] = info.context["request"]
        authorization = request.headers.get('Authorization')
        jwtSecret = os.environ.get('JWT_SECRET')

        if "Authorization" in request.headers:
            auth = jwt.decode(authorization, jwtSecret, algorithms="HS256")
            return auth

        return False

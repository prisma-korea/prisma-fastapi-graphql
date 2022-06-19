from datetime import time
import os
from typing_extensions import Self
import jwt
from typing import Dict
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

jwtSecret = os.environ.get('JWT_SECRET')


def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "userId": user_id,
        "expires": time().second + 600
    }
    token = jwt.encode(payload, jwtSecret, algorithm='HS256')

    return token


def decodeJWT(token: str) -> dict:
    try:
        decoded = jwt.decode(token, jwtSecret, algorithms=['HS256'])
        return decoded if decoded["expires"] >= time().second else None
    except:
        return {}


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtToken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtToken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid

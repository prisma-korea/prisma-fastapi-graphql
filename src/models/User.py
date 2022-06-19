from datetime import date
from typing import Optional
import strawberry

from src.models.scalars import Gender


@strawberry.type
class User:
    id: strawberry.ID
    email: str
    name: Optional[str] = None
    nickname: Optional[str] = None
    thumbURL: Optional[str] = None
    photoURL: Optional[str] = None
    birthday: Optional[date] = None
    gender: Optional[Gender] = None
    phone: Optional[str] = None


@strawberry.type
class AuthPayload:
    token: str
    user: User

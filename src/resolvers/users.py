import datetime
from typing import List, Optional
from src.models.User import AuthPayload, User
from src.prisma import prisma
import strawberry
from src.models.scalars import Gender

from src.permission import IsAuthenticated

@strawberry.type
class Query:
    @strawberry.field(permission_classes=[IsAuthenticated])
    def users(self) -> List[User]:
        return prisma.user.find_many()

    @strawberry.field(permission_classes=[IsAuthenticated])
    def user(self, id: strawberry.ID) -> User:
        return prisma.user.find_unique(
            where={
                "id": id
            }
        )


@strawberry.input
class UserCreateInput:
    email: str
    password: str
    name: Optional[str] = None
    nickname: Optional[str] = None
    birthday: Optional[datetime.date] = None
    gender: Optional[Gender] = None
    phone: Optional[str] = None


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def signIn(self, email: str, password: str) -> AuthPayload:
        user = await prisma.user.find_first(
            where={
                "email": email,
                "password": password,
            }
        )

        return AuthPayload(token="token", user=user)

    @strawberry.mutation
    def signUp(self, user: UserCreateInput) -> User:
        user = prisma.user.create({
            "email": user.email,
            "password": user.password,
            "name": user.name,
            "nickname": user.nickname,
            "birthDay": user.birthday,
            "gender": user.gender,
            "phone": user.phone,
        })

        return user

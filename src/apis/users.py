from typing import List
from fastapi import APIRouter, Depends
from src.models.User import User
from src.prisma import prisma
from src.utils.auth import JWTBearer, decodeJWT

router = APIRouter()


@router.get("/users/", tags=["users"])
async def read_users():
    users: List[User] = await prisma.user.find_many()

    for (user) in users:
        del user.password

    return users


@router.get("/users/me", tags=["users"])
async def read_user_me(token=Depends(JWTBearer())):
    decoded = decodeJWT(token)

    if 'userId' in decoded:
        userId = decoded['userId']
        return await prisma.user.find_unique(
            where={
                "id": userId
            }
        )
    return None


@router.get("/users/{userId}", tags=["users"])
async def read_user(userId: str):
    user = await prisma.user.find_unique(
        where={"id": userId}
    )

    return user

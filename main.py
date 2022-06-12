from src.apis import apis
from src.resolvers import schema
from typing import Union
from prisma import Prisma

import strawberry
from fastapi import FastAPI
from strawberry.asgi import GraphQL
from fastapi import FastAPI


graphql_app = GraphQL(schema)

prisma = Prisma()
app = FastAPI()
# app.add_middleware(GZipMiddleware, minimum_size=1000)
app.include_router(apis, prefix='/apis')
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)


@app.on_event("startup")
async def startup():
    await prisma.connect()


@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()


@app.get("/")
async def read_root():
    users = await prisma.user.find_many()
    return {"users": users}

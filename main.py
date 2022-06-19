import os
import jwt
from src.prisma import prisma
from src.apis import apis
from src.resolvers import schema

from fastapi import FastAPI
from strawberry.asgi import GraphQL as BaseGraphQL
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.gzip import GZipMiddleware


class GraphQL(BaseGraphQL):
    async def get_context(self, request, response):
        headers = request.headers
        tokenIsPresent = headers.get('Authorization', False)

        if tokenIsPresent:
            jwtSecret = os.environ.get('JWT_SECRET')
            decoded = jwt.decode(tokenIsPresent, jwtSecret, algorithms="HS256")

            if 'userId' in decoded:
                return {
                    "userId": decoded['userId'],
                    "request": request,
                }


load_dotenv()
graphql_app = GraphQL(schema)

app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=1000)
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

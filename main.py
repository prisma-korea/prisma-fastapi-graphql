import os
from src.prisma import prisma
from src.apis import apis
from src.resolvers import schema

from fastapi import FastAPI
from strawberry.asgi import GraphQL as BaseGraphQL
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.gzip import GZipMiddleware

from src.utils.auth import decodeJWT


class GraphQL(BaseGraphQL):
    async def get_context(self, request, response):
        headers = request.headers
        tokenIsPresent = headers.get('Authorization', False)

        if tokenIsPresent:
            decoded = decodeJWT(tokenIsPresent)

            if 'userId' in decoded:
                return {
                    "userId": decoded['userId'],
                    "request": request,
                }


load_dotenv()
isProduction = os.getenv("IS_PRODUCTION", False)

graphql_app = GraphQL(schema, graphiql=False if isProduction else True)

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
    return {"version": "1.0.0"}

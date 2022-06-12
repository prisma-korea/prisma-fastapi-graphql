from src.resolvers.users import Query
import strawberry


schema = strawberry.Schema(query=Query)

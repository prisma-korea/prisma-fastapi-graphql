from src.resolvers.users import Query, Mutation
import strawberry


schema = strawberry.Schema(query=Query, mutation=Mutation)

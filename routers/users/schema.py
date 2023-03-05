import strawberry
from strawberry.asgi import GraphQL

from . import mutations
from . import queries

schema = strawberry.Schema(query=queries.Query,mutation=mutations.Mutation)
graphql_app = GraphQL(schema)
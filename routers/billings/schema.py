import strawberry
from strawberry.asgi import GraphQL

from . import queries

schema = strawberry.Schema(query=queries.Query)
graphql_app = GraphQL(schema)
import strawberry
from strawberry.asgi import GraphQL

from . import mutations
from . import queries
from . import types

schema = strawberry.Schema(query=queries.Query,mutation=mutations.Mutation, types=[types.DateTime])
graphql_app = GraphQL(schema)
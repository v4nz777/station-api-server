from fastapi import FastAPI, Response
from routers.users import users,schema_users
# from starlette_graphene3
import os
import utils
import json
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

app.include_router(
    users.router,
    prefix='/users',
    tags=['users']
)

app.add_route("/graphql/users", schema_users.graphql_app)

@app.get('/')
async def root()-> Response:
    return Response(json.dumps({'hello':'world'}))

@app.on_event('startup')
async def generate_fernet_key()->None:
    if not 'FERNET_KEY' in os.environ:
        os.environ['FERNET_KEY'] = utils.get_key_from_file().decode('utf-8')

   





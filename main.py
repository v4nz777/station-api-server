from fastapi import FastAPI, Response
from routers.users import schema as userschema
from routers.ads import schema as adschema
from routers.adspackages import schema as adspackageschema
from routers.billings import schema as billingschema
from dotenv import load_dotenv
import os
import utils
import json


load_dotenv()
app = FastAPI()


app.add_route("/graphql/users", userschema.graphql_app)
app.add_route("/graphql/ads", adschema.graphql_app)
app.add_route("/graphql/adspackages", adspackageschema.graphql_app)
app.add_route("/graphql/billings", billingschema.graphql_app)


@app.get('/')
async def root()-> Response:
    return Response(json.dumps({'hello':'world'}))

@app.on_event('startup')
async def generate_fernet_key()->None:
    if not 'FERNET_KEY' in os.environ:
        os.environ['FERNET_KEY'] = utils.get_key_from_file().decode('utf-8')

   





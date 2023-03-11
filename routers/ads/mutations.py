import json
import strawberry
from . import helpers
from .types import Advertisement,AdCreationInput, VersionDetail
import datetime
from jwt_auth import require_token


@strawberry.type
class Mutation:

    @strawberry.mutation
    @require_token
    def create_new_ad(self,info,adsdetail:AdCreationInput)->Advertisement:
        created = helpers.add_ad_to_database(adsdetail)
        return helpers.ad_dict_to_advertisement(created)
    
    @strawberry.mutation
    @require_token
    def update_ad(self,info,contract:str,stringified_update:str)->Advertisement:
        jsoned_update = json.loads(stringified_update)
        updated = helpers.update_ad_in_database(contract,jsoned_update)
        return helpers.ad_dict_to_advertisement(updated)

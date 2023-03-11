import json
import strawberry
from . import helpers
from .types import Advertisement,AdCreationInput, VersionDetail
import datetime
from jwt_auth import require_token
import loggings


@strawberry.type
class Mutation:

    @strawberry.mutation
    @require_token
    def create_new_ad(self,info,author:str,adsdetail:AdCreationInput)->Advertisement:
        created = helpers.add_ad_to_database(adsdetail)
        if created:
            loggings.log_user_actions(author,f'Added a new contract {adsdetail.contract}')
        return helpers.ad_dict_to_advertisement(created)
    
    @strawberry.mutation
    @require_token
    def update_ad(self,info,author:str,contract:str,stringified_update:str)->Advertisement:
        jsoned_update = json.loads(stringified_update)
        updated = helpers.update_ad_in_database(author,contract,jsoned_update)
        if updated:
            loggings.log_user_actions(author, f'Made some changes to ad contract {contract}')
        return helpers.ad_dict_to_advertisement(updated)

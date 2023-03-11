from typing import List
import strawberry
from . import helpers
from .types import Advertisement
import loggings
from jwt_auth import require_token


@strawberry.type
class Query:

    @strawberry.field
    @require_token
    def get_all_ads(self, info)->List[Advertisement]:
        return helpers.get_all_ads_as_advertisements()
    
    @strawberry.field
    @require_token
    def get_ad(self,info,contract:str)->Advertisement:
        ad_from_db = helpers.get_ad_from_database(contract)
        return helpers.ad_dict_to_advertisement(ad_from_db)
    
    
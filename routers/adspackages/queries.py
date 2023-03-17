import strawberry
from jwt_auth import require_token
from .types import AdsPackage
from typing import List
from . import helpers

@strawberry.type
class Query:

    @strawberry.field
    @require_token
    def get_all_packages(self,info) -> List[AdsPackage]:
        return helpers.get_all_ads_as_ads_packages()


    @strawberry.field
    @require_token
    def get_package(self,info,title:str) -> AdsPackage:
        return helpers.get_ads_package(title)

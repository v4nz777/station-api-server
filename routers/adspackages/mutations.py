import strawberry
from .types import AdsPackageCreationInput,AdsPackage
from typing import List
from . import helpers
from jwt_auth import require_token


@strawberry.type
class Mutation:

    @strawberry.field
    def create_ads_package(self,info,details:AdsPackageCreationInput)->AdsPackage:
        return helpers.add_ads_package_to_database(details)

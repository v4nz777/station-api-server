from db import MainDB
from typing import Any,List
from .types import AdsPackage,AdsPackageCreationInput
from routers.ads.types import VersionDetail
from strawberry.file_uploads import Upload


def get_all_ads_as_ads_packages()->List[AdsPackage|Any]:
    _all = []
    for i in get_all_packages_from_database():
        _all.append(dict_to_package(i))
    return _all

def get_ads_package(title:str)->AdsPackage:
    package = get_package_from_database(title)
    if not package:
        raise ValueError(f'Cannot find package: {title}')
    return AdsPackage(**package)

def get_package_from_database(title:str)->str:
    db = connect_to_database_collection_adspackages()
    return db.read({'title':title})
    

def get_all_packages_from_database()->List[dict]:
    db = connect_to_database_collection_adspackages()
    return db.read_all()


def dict_to_package(data:dict)->AdsPackage:
    return AdsPackage(**data)


def add_ads_package_to_database(package:AdsPackageCreationInput)->AdsPackage:
    item = package.jsonify()
    db = connect_to_database_collection_adspackages()
    if get_package_from_database(package.title):
        raise ValueError('Package already exist in database')
    return dict_to_package(db.create(item))


def connect_to_database_collection_adspackages()->MainDB:
    db:MainDB = MainDB() # Instatiates database connection
    db.create_collection('ads_packages') # Will create new collection if it doesnt exist yet
    db.to_collection('ads_packages') # Then connects to the collection
    return db
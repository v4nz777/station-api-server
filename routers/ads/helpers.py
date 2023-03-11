from db import MainDB
from typing import Any,List
from jose import jwt
import datetime
from .types import AdCreationInput,Advertisement,VersionDetail
import loggings

def get_all_ads_as_advertisements()->List[Advertisement|Any]:
    _all = []
    for i in get_all_ads_from_database():
        _all.append(ad_dict_to_advertisement(i))
    return _all

def ad_dict_to_advertisement(ad_from_database:dict)->Advertisement:
    details = VersionDetail(**ad_from_database['details'])
    prev_vers = [VersionDetail(**ver) for ver in ad_from_database['prev_versions']]
    return Advertisement(
        _id=ad_from_database['_id'],
        title=ad_from_database['title'],
        type=ad_from_database['type'],
        contract=ad_from_database['contract'],
        bo=ad_from_database['bo'],
        created=ad_from_database['created'],
        updated=ad_from_database['updated'],
        details=details,
        prev_versions=prev_vers
    )

def get_all_ads_from_database()->List[dict|Any]:
    db = connect_to_database_collection_ads()
    ads = db.read_all()
    return ads

def get_ad_from_database(contract:str)->dict|None:
    db = connect_to_database_collection_ads()
    data =  db.read({'contract':contract})
    if data:
        return data
    else:
        raise ValueError('Contract not found!')

def add_ad_to_database(input:AdCreationInput)->dict:
    data= input.jsonify()
    if get_ad_from_database(data.get('contract')): # Check if already exists
        raise ValueError('Contract already in database')
    db = connect_to_database_collection_ads()
    
    # Set default values before saving
    data['created'] = datetime.datetime.now()
    data['updated'] = None
    data['prev_versions'] = []
    data['details']['stashed'] = None
    data['details']['version'] = 1

    return  db.create(data)


def update_ad_in_database(contract:str,update:dict)->dict:
    db = connect_to_database_collection_ads()
    stashed_version,versions_count = stash_current_version(contract,db)
    update['version'] = versions_count + 1
    return db.update({'contract':contract},{'details':update,'updated':datetime.datetime.now()})


def stash_current_version(contract:str,db:MainDB) -> tuple:
    """Returns the `latest details` and `number of total versions`"""
    current_versions:List[dict] = []
    # Update the current state
    subject = db.read({'contract':contract},exclude=['_id']) # get current state
    if not subject:
        raise ValueError('Contract not found!')
    current_versions = subject['prev_versions'] # Save versions list to new variable
    del subject['prev_versions'] # This prevents from messing up with the versions
    subject['stashed'] = datetime.datetime.now()
    # Add current state to the versions list.
    current_versions.append(subject['details'])
    updated = db.update({'contract':contract},{'prev_versions':current_versions})
    return updated['details'],len(updated['prev_versions'])



def connect_to_database_collection_ads()->MainDB:
    db:MainDB = MainDB() # Instatiates database connection
    db.create_collection('ads') # Will create new collection if it doesnt exist yet
    db.to_collection('ads') # Then connects to the collection
    return db
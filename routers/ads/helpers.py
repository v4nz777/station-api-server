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
    return db.read({'contract':contract})


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


def stash_current_version(contract:str,db:MainDB|None = None) -> tuple:
    """Returns the `latest details` and `number of total versions`"""
    if not db:
        db = connect_to_database_collection_ads()

    # Get the current state of the contract
    subject = db.read({'contract':contract},exclude=['_id'])
    if not subject:
        raise ValueError('Contract not found!')
    
    # Save current versions to variable, then delete to the subject to prevent messing it up
    current_versions = subject.get('prev_versions',[])
    del subject['prev_versions']
    subject['details']['stashed'] = datetime.datetime.now()

    # Add current state to the versions list but prevents duplicate versions.
    current_versions.append(subject['details'])
    updated = db.update({'contract':contract},{'prev_versions':get_unique_from_list_of_dicts(current_versions)})
    return updated['details'],len(updated['prev_versions'])

def get_unique_from_list_of_dicts(obj_list:List[dict])->List[dict]:
    unique_objects = []  # The list of unique objects
    versions = set()  # The set of version numbers seen so far

    for obj in obj_list:
        if obj['version'] not in versions:
            unique_objects.append(obj)
            versions.add(obj['version'])

    return unique_objects

def use_ad_version(contract:str, use_version:int)-> dict:
    """Apply the details based on the previous version available"""
    db = connect_to_database_collection_ads()
    current_ad = get_ad_from_database(contract=contract)

    if not current_ad:
        raise ValueError('Contract does not exist')
    
    if current_ad['details']['version'] == use_version:
        raise ValueError('This version is currently in use')
    
    selected = [ver for ver in current_ad['prev_versions'] if ver['version'] == use_version][0]
    stash_current_version(contract, db)
    return db.update({'contract':contract},{'details':selected,'updated':datetime.datetime.now()})

def connect_to_database_collection_ads()->MainDB:
    db:MainDB = MainDB() # Instatiates database connection
    db.create_collection('ads') # Will create new collection if it doesnt exist yet
    db.to_collection('ads') # Then connects to the collection
    return db
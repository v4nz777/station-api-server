from db import MainDB
from typing import Dict,Any,List
import json
from .schema_users import UserCreationInput


def get_all_users()->List[dict|Any]:
    db = connect_to_database_collection_users()
    users = db.read_all()
    return users

def get_user(username:str)->dict|None:
    db = connect_to_database_collection_users()
    return check_existing_username(username,db)

def create_user(userdata:UserCreationInput)->dict:
    db = connect_to_database_collection_users()
    if check_existing_username(userdata.username,db):
        raise ValueError(f"{userdata.username} already existed in database")
    secured_userdata = handle_with_secure_user_creation(userdata.jsonify(),db)
    return db.create(secured_userdata)

def update_user(username:str,update:dict)->dict:
    query = {'username':username}
    db = connect_to_database_collection_users()
    secured_update = handle_with_secure_user_update(query,update,db)
    return db.update(query,secured_update)

def handle_with_secure_user_creation(document:dict,db:MainDB)->dict:
    if document.get('password'):
        document['password'] = db.encode_password(document.get('password'))
    return document

def handle_with_secure_user_update(query:dict,update:dict,db:MainDB)->dict:
    if update.get('new_password') and update.get('password'):
        if db.authenticate_password(query,update.get('password')):
            update['password'] = db.encode_password(update.get('new_password'))
            del update['new_password']
        else:
            raise ValueError('Wrong password!')
    elif update.get('password') and not update.get('new_password'):
        del update['password']
    elif not update.get('password') and update.get('new_password'):
        del update['new_password']
    return update

def get_json_string_of_user(username:str)->str:
    db = connect_to_database_collection_users()
    userdetails = check_existing_username(username,db)
    return json.dumps(userdetails,cls=db.OBjectIDtoStringConverter)

def create_user_and_get_json_string(userdata:dict)->str:
    create_user(userdata)
    return get_json_string_of_user(userdata['username'])

def check_existing_username(value:str,db:MainDB)->Any:
    try:
        return db.read({'username':value})
    except TypeError:
        return None

def connect_to_database_collection_users()->MainDB:
    db:MainDB = MainDB() # Instatiates database connection
    db.create_collection('users') # Will create new collection if it doesnt exist yet
    db.to_collection('users') # Then connects to the collection
    return db


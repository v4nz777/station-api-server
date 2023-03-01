from db import MainDB
from typing import Dict,Any
import json


def get_json_string_of_user(username:str)->str:
    db = connect_to_database_collection_users()
    userdetails = check_existing_username(username,db)
    return json.dumps(userdetails,cls=db.OBjectIDtoStringConverter)

def create_user_and_get_json_string(userdata:dict)->str:
    username = userdata['username']
    db = connect_to_database_collection_users()
    if check_existing_username(username,db):
        return None
    db.create(userdata)
    return get_json_string_of_user(username)

def connect_to_database_collection_users()->MainDB:
    db:MainDB = MainDB()
    db.to_collection('users')
    return db

def check_existing_username(value:str,db:MainDB)->Any:
    try:
        return db.read({'username':value})
    except TypeError:
        return None


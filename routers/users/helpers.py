from db import MainDB
from typing import Any,List
from jose import jwt
from .types import UserCreationInput
import datetime
import utils
import loggings
import os


def get_all_users_from_database()->List[dict|Any]:
    db = connect_to_database_collection_users()
    users = db.read_all()
    return users

def get_user_from_database(username:str)->dict|None:
    db = connect_to_database_collection_users()
    return check_existing_username(username,db)

def add_user_to_database(userdata:UserCreationInput)->dict:
    db = connect_to_database_collection_users()
    if check_existing_username(userdata.username,db):
        raise ValueError(f"{userdata.username} already existed in database")
    secured_userdata = handle_with_secure_user_creation(userdata.jsonify(),db)
    return db.create(secured_userdata)

def update_user_in_database(username:str,update:dict)->dict:
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
        # if validate_user(query['username'],update.get('password'))
            update['password'] = db.encode_password(update.get('new_password'))
            del update['new_password']
        else:
            raise ValueError('Wrong password!')
    elif update.get('password') and not update.get('new_password'):
        del update['password']
    elif not update.get('password') and update.get('new_password'):
        del update['new_password']
    return update

def validate_user(username:str, password:str, db:MainDB=None) -> bool:
    if db is None:
        db = connect_to_database_collection_users()
    return db.authenticate_password({'username':username},password)


def check_existing_username(value:str,db:MainDB)->Any:
    try:
        return db.read({'username':value})
    except TypeError:
        return None
    
def handle_login(username:str) ->dict:
    update = {
        'last_login': datetime.datetime.now(),
        'status': 'active'
    }
    loggings.log_user_actions(username=username , action='Logged in')
    return update_user_in_database(username,update)

def handle_logout(username:str) -> dict:
    update = {
        'last_logout': datetime.datetime.now(),
        'status': 'away'
    }
    updated_user = update_user_in_database(username,update)
    summary = log_user(updated_user)
    loggings.log_user_actions(username=username , action='Logged out')
    return summary

def log_user(latest_state: dict)->dict:
    username = latest_state['username']
    last_login: datetime.datetime = latest_state['last_login']
    last_logout: datetime.datetime = latest_state['last_logout']

    return loggings.write_user_log({
        'username':username,
        'login':last_login,
        'logout':last_logout,
        'total_shift': utils.get_total_duty(last_login,last_logout),
        'total_overtime':utils.get_overtime_duty(last_login,last_logout),
        'total_night_shift':utils.get_night_shift(last_login,last_logout),
    })
 
def generate_jwt(payload:dict,key:str):
    if not key:
        key = os.environ['FERNET_KEY']
    return jwt.encode(payload,key,algorithm='HS256')

def connect_to_database_collection_users()->MainDB:
    db:MainDB = MainDB() # Instatiates database connection
    db.create_collection('users') # Will create new collection if it doesnt exist yet
    db.to_collection('users') # Then connects to the collection
    return db


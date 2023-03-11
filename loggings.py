from db import MainDB
import datetime

def write_user_log(latest_state:dict) -> dict:
    db = connect_to_database_collection_loggings_users()

    return db.create(latest_state)

def get_user_logs_all(username:str)-> dict:
    db = connect_to_database_collection_loggings_users()
    return db.read_all(username=username)

def log_user_actions(username:str, action:str)->dict:
    db = connect_to_database_collection_actions_users()
    return db.create({
        'username': username,
        'action': action,
        'happens': datetime.datetime.now()
    })

def connect_to_database_collection_loggings_users()->MainDB:
    db:MainDB = MainDB() # Instatiates database connection
    db.create_collection('users_log') # Will create new collection if it doesnt exist yet
    db.to_collection('users_log') # Then connects to the collection
    return db

def connect_to_database_collection_actions_users()->MainDB:
    db:MainDB = MainDB() # Instatiates database connection
    db.create_collection('users_actions') # Will create new collection if it doesnt exist yet
    db.to_collection('users_actions') # Then connects to the collection
    return db
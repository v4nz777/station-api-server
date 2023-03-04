from db import MainDB

def log_user_logging_activity(latest_state:dict) -> dict:
    db = connect_to_database_collection_loggings_users()
    return db.create(latest_state)

def get_user_logs_all(username:str)-> dict:
    db = connect_to_database_collection_loggings_users()
    return db.read_all(username=username)

def connect_to_database_collection_loggings_users()->MainDB:
    db:MainDB = MainDB() # Instatiates database connection
    db.create_collection('users_log') # Will create new collection if it doesnt exist yet
    db.to_collection('users_log') # Then connects to the collection
    return db
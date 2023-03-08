import json
import strawberry
from . import helpers
from .types import User,UserCreationInput,UserLog, AccessToken
import datetime
import jwt_auth

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(self, info, userdata:UserCreationInput) -> User:
        created = helpers.add_user_to_database(userdata)   
        return User(**created)
    
    @strawberry.mutation 
    def update_user(self,info,username:str,update:str)-> User:
        """When updating password, include both fields: `password` and `new_password`"""
        jsoned_update = json.loads(update)
        jsoned_update['updated'] = datetime.datetime.now()

        db = helpers.connect_to_database_collection_users() # intialize connection to collection, users
        if not helpers.check_existing_username(username,db):
            raise ValueError(f'{username} does not exist in database')
        helpers.update_user_in_database(username,jsoned_update)
        updated_user = db.read({'username': username})
        return User(**updated_user)
    
    @strawberry.mutation
    def get_access_token(self,info,username:str,password:str)-> AccessToken:
        if helpers.validate_user(username,password):
            return AccessToken(username=username,access_token=jwt_auth.encode_jwt_token(username))
        raise ValueError('Wrong password')

    @strawberry.mutation
    def login_user(self, info, username:str)-> User:
        logged_user = helpers.handle_login(username)  
        return User(**logged_user)

    @strawberry.mutation
    def logout_user(self, info, username:str)-> UserLog:
        summary = helpers.handle_logout(username)
        return UserLog(**summary)

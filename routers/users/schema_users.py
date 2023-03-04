import json
from typing import List
from strawberry.asgi import GraphQL
import strawberry
from . import helpers
import loggings
import datetime


@strawberry.type
class User:
    username: str
    password:str
    email:str
    _id:str
    email:str|None
    address:str|None
    mobile:str|None
    status:str
    created:datetime.datetime
    updated:datetime.datetime | None
    last_login:datetime.datetime | None
    last_logout:datetime.datetime | None


@strawberry.type
class UserLog:
    _id:str
    username:str
    login:datetime.datetime
    logout:datetime.datetime|None
    total_shift:List[int]
    total_overtime:List[int]
    total_night_shift:List[int]

@strawberry.input
class UserCreationInput:
    username:str
    password:str
    email:str|None = None
    address:str|None = None
    mobile:str|None = None
    status:str = 'away' # Options: `away` `active` `inactive`
    created:datetime.datetime = datetime.datetime.now()
    updated:datetime.datetime|None = None
    last_login:datetime.datetime | None = None
    last_logout:datetime.datetime | None = None
    
    def jsonify(self)->dict:
        return {
            "username":self.username,
            "password":self.password,
            "email":self.email,
            "address":self.address,
            "mobile":self.mobile,
            "status":self.status,
            "created":self.created,
            "updated":self.updated,
            "last_login": self.last_login,
            "last_logout": self.last_logout,
        }


@strawberry.type
class Query:
    @strawberry.field
    def all_users(self, info) -> List[User]:
        return [User(**user) for user in helpers.get_all_users()]

    @strawberry.field
    def user(self, info, username: str)-> User:
        return User(**helpers.get_user(username))
    
    @strawberry.field
    def all_user_logs(self, info, username:str)-> List[UserLog]:
        return [UserLog(**userlogs) for userlogs in loggings.get_user_logs_all(username)]
    
@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(self, info, userdata:UserCreationInput) -> User:
        created = helpers.create_user(userdata)   
        return User(**created)
    
    @strawberry.mutation 
    def update_user(self,info,username:str,update:str)-> User:
        """When updating password, include both fields: `password` and `new_password`"""
        jsoned_update = json.loads(update)
        jsoned_update['updated'] = datetime.datetime.now()
        db = helpers.connect_to_database_collection_users()
        if not helpers.check_existing_username(username,db):
            raise ValueError(f'{username} does not exist in database')
        helpers.update_user(username,jsoned_update)
        updated_user = db.read({'username': username})
        return User(**updated_user)
    
    @strawberry.mutation
    def login_user(self, info, username:str)-> User:
        logged_user = helpers.handle_login(username)  
        return User(**logged_user)

    @strawberry.mutation
    def logout_user(self, info, username:str)-> UserLog:
        summary = helpers.handle_logout(username)
        return UserLog(**summary)

schema = strawberry.Schema(query=Query,mutation=Mutation)
graphql_app = GraphQL(schema)

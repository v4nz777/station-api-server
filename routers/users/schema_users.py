import json
from typing import List
from strawberry.asgi import GraphQL
import strawberry
from . import helpers


@strawberry.type
class User:
    username: str
    password:str
    email:str
    _id:str
    

@strawberry.input
class UserCreationInput:
    username:str
    password:str
    email:str
    optional:str|None = None
    
    def jsonify(self)->dict:
        return {
            "username":self.username,
            "password":self.password,
            "email":self.email,
        }
    

@strawberry.type
class Query:
    @strawberry.field
    def all_users(self, info) -> List[User]:
        return [User(**user) for user in helpers.get_all_users()]

    @strawberry.field
    def user(self, info, username: str)-> User:
        return User(**helpers.get_user(username))
    
@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(self, info, userdata:UserCreationInput) -> User:
        created = helpers.create_user(userdata)   
        return User(**created)
    
    @strawberry.mutation 
    def update_user(self,info,username:str,update:str)-> User:
        jsoned_update = json.loads(update)
        db = helpers.connect_to_database_collection_users()

        if not helpers.check_existing_username(username,db):
            raise ValueError(f'{username} does not exist in database')
        
        helpers.update_user(username,jsoned_update)
        updated_user = db.read({'username': username})
        return User(**updated_user)
        

schema = strawberry.Schema(query=Query,mutation=Mutation)
graphql_app = GraphQL(schema)

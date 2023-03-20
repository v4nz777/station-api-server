from typing import List
import strawberry
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
    display:str|None = None


@strawberry.type
class UserLog:
    _id:str
    username:str
    login:datetime.datetime
    logout:datetime.datetime|None
    total_shift:List[int]
    total_overtime:List[int]
    total_night_shift:List[int]


@strawberry.type
class AccessToken:
    username:str
    access_token:str


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




    


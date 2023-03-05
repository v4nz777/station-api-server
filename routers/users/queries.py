from typing import List
import strawberry
from . import helpers
from .types import User,UserLog
import loggings


@strawberry.type
class Query:
    @strawberry.field
    def all_users(self, info) -> List[User]:
        return [User(**user) for user in helpers.get_all_users_from_database()]

    @strawberry.field
    def user(self, info, username: str)-> User:
        return User(**helpers.get_user_from_database(username))
    
    @strawberry.field
    def all_user_logs(self, info, username:str)-> List[UserLog]:
        return [UserLog(**userlogs) for userlogs in loggings.get_user_logs_all(username)]

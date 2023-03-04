import pymongo
from typing import Dict, Any, List
import os
import json
from bson import ObjectId
from cryptography.fernet import Fernet

class MainDB:
    def __init__(self, uri:str|None=None) -> None:
        """
        Include the dbname for uri of db. example: `mongodb://localhost:27017/dbname`
        """
        if uri:
            self.client: pymongo.MongoClient = pymongo.MongoClient(uri)
        else:
            self.client: pymongo.MongoClient = pymongo.MongoClient(os.environ['DB_URL'])
        self.db: pymongo.database.Database = self.client.get_database()

    def create_collection(self,name:str):
        if name not in self.db.list_collection_names():
            self.db.create_collection(name)

    def to_collection(self, collection:str)-> Any:
        self.collection: pymongo.collection.Collection = self.db.get_collection(collection)
        return self.collection


    def create(self, document: Dict[str, Any]) -> Any:
        result: pymongo.results.InsertOneResult = self.collection.insert_one(document)
        return self.read({'_id':result.inserted_id})


    def read(self, query: Dict[str, Any],**kwargs) -> Dict[str, Any]:
        """add `exclude=[password,...yourfield]` to exclude fields"""
        exclude = kwargs.get('exclude',['_'])
        exempted = self.exempt_fields(exclude)
        result: pymongo.cursor.Cursor = self.collection.find_one(query,exempted)
        return dict(result)
    

    def read_all(self,**kwargs) -> List[Dict[str, Any]]:
        """
            - To filter by user, add `username='your_username'`
            - Add `exclude=[password,...yourfield]` to exclude fields
        """
        query = {}
        if kwargs.get('username'):
            query['username'] = kwargs.get('username')
        exclude = kwargs.get('exclude',['_'])
        exempted = self.exempt_fields(exclude)
        result: pymongo.cursor.Cursor = self.collection.find(query,exempted)
        return list(result)
    

    def update(self, query: Dict[str, Any],update: Dict[str, Any]) -> dict:
        # Ensure that update uses valid MongoDB update syntax

        if not any(key.startswith('$') for key in update.keys()):
            update = {'$set': update}
        
        self.collection.update_many(query, update)
        return self.read(query)


    def delete(self, query: Dict[str, Any]) -> int:
        result: pymongo.results.DeleteResult = self.collection.delete_many(query)
        return result.deleted_count
    

    def encode_password(self,string:str)->bytes:
        password_encoder = Fernet(os.environ['FERNET_KEY'])
        return password_encoder.encrypt(string.encode('utf-8'))


    def decode_password(self,bytevalue:bytes)->str:
        password_decoder = Fernet(os.environ['FERNET_KEY'])
        return password_decoder.decrypt(bytevalue).decode('utf-8')


    def authenticate_password(self,query:dict,entry:str) -> bool:
        current_password:bytes = self.read(query,exclude=['_'])['password']
        return self.decode_password(current_password) == entry
        

    def exempt_fields(self,exemptions:List[str])->dict:
        projection = {}
        for field in exemptions:
            projection[field]=False
        return projection
    
    def byte_to_string(self,value:bytes)->str:
        return value.decode('utf-8')

    class OBjectIDtoStringConverter(json.JSONEncoder):
        def default(self, obj)->str:
            if isinstance(obj, ObjectId):
                return str(obj)
            return json.JSONEncoder.default(self, obj)
    



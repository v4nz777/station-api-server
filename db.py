import pymongo
from typing import Dict, Any, List, Optional
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
        
    def to_collection(self, collection:str)-> Any:
        self.collection: pymongo.collection.Collection = self.db.get_collection(collection)
        return self.collection

    def create(self, document: Dict[str, Any]) -> Any:
        if document.get('password'):
            document['password'] = self.encode_password(document.get('password'))
        result: pymongo.results.InsertOneResult = self.collection.insert_one(document)
        return result.inserted_id

    def read(self, query: Dict[str, Any],**kwargs) -> Dict[str, Any]:
        """add `exclude=[password,...yourfield]` to exclude fields, default `['password']`"""
        exclude = kwargs.get('exclude',['password'])

        exempted = self.exempt_fields(exclude)
        result: pymongo.cursor.Cursor = self.collection.find_one(query,exempted)
        return dict(result)
    
    def read_all(self,**kwargs) -> List[Dict[str, Any]]:
        """add `exclude=[password,...yourfield]` to exclude fields, default `['password']`"""
        exclude = kwargs.get('exclude',['password'])
        
        exempted = self.exempt_fields(exclude)
        result: pymongo.cursor.Cursor = self.collection.find({},exempted)
        return list(result)
    
    def update(self, query: Dict[str, Any], update: Dict[str, Any]) -> bool:
        if update.get('password'):
            if self.authenticate_password(query,update.get('old_password')):
                update['password'] = self.encode_password(update.get('password'))
                del update['old_password']
            else:
                return False
            
        # Ensure that update uses valid MongoDB update syntax
        if not any(key.startswith('$') for key in update.keys()):
            update = {'$set': update}
        
        self.collection.update_many(query, update)
        return True

    def delete(self, query: Dict[str, Any]) -> int:
        result: pymongo.results.DeleteResult = self.collection.delete_many(query)
        return result.deleted_count
    
    def encode_password(self,string:str)->bytes:
        password_encoder = Fernet(os.environ['FERNET_KEY'])
        return password_encoder.encrypt(string.encode('utf-8'))

    def decode_password(self,bytes:bytes)->str:
        password_decoder = Fernet(os.environ['FERNET_KEY'])
        return password_decoder.decrypt(bytes).decode('utf-8')

    def authenticate_password(self,query:dict,entry:str) -> bool:
        old_pass:bytes = self.read(query,exclude=['_'])['password']
        return self.decode_password(old_pass) == entry
        

    def exempt_fields(self,exemptions:List[str])->dict:
        projection = {}
        for field in exemptions:
            projection[field]=False
        return projection

    class OBjectIDtoStringConverter(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, ObjectId):
                return str(obj)
            return json.JSONEncoder.default(self, obj)
    



from fastapi import APIRouter, Response
from . import helpers
from typing import Dict,Any

import json

router = APIRouter()

@router.get('/')
async def get_all_users()-> Response:
    db = helpers.connect_to_database_collection_users()
    json_string = json.dumps(db.read_all(),cls=db.OBjectIDtoStringConverter)
    return Response(content=json_string,media_type='application/json')


@router.get('/{username}')
async def get_user(username:str)-> Response:
    json_string = helpers.get_json_string_of_user(username)
    return Response(content=json_string,media_type='application/json')


@router.post('/create')
async def create_new_user(userdata:Dict[str, Any])-> Response:
    json_string = helpers.create_user_and_get_json_string(userdata)
    if not json_string:
        return Response(content={'error':'There is an error creating user'},media_type='application/json',status_code=400)
    return Response(content=json_string,media_type='application/json')


@router.put('/update/{username}')
async def update_user_details(username: str, userdata: Dict[str, Any]) -> Response:
    db = helpers.connect_to_database_collection_users()
    
    if not helpers.check_existing_username(username,db):
        json_string = json.dumps({'error': f'{username} does not exist in database'})
        return Response(content=json_string, media_type='application/json', status_code=404)
    
    if db.update({'username': username}, userdata):
        updated_user = db.read({'username': username})
        json_string = json.dumps(updated_user, cls=db.OBjectIDtoStringConverter)
        return Response(content=json_string, media_type='application/json')
    
    else:
        json_string=json.dumps({'error':'Wrong password'})
        return Response(content=json_string,media_type='application/json',status_code=400)

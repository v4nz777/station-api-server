from functools import wraps
from typing import Callable
from jose import jwt
import os
import datetime



def require_token(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, info, **kwargs):
        authorization = info.context['request'].headers.get('authorization')
        if authorization is None:
            raise ValueError('Authorization header missing')
        token = authorization.split(' ')[1]
        try:
            # Decode and verify the JWT token here
            # If the token is invalid or expired, raise an exception
            # If the token is valid, extract the user information from the token and pass it to the wrapped function
            user_info = decode_and_verify_jwt_token(token)
        except:
            raise ValueError('Invalid or expired token')
 
        # Call the wrapped function with the extracted user information
        return func(*args, info=user_info, **kwargs)
    return wrapper


def decode_and_verify_jwt_token(token: str) -> dict:
    secret_key = os.environ['FERNET_KEY']
    try:
        # Decode the JWT token using the secret key
        decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
    except:
        # If the token is invalid or expired, raise an exception
        raise Exception('Invalid or expired token')
    
    # Return the decoded token as a dictionary
    return decoded_token

def encode_jwt_token(username: str, expiration_days: int = 1) -> str:

    # Calculate the expiration time for the token
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=expiration_days)
    
    # Create the payload for the token
    payload = {
        'username': username,
        'expiration': expiration_time.isoformat()
    }

    # Encode the payload and sign the token using the secret key
    token = jwt.encode(payload, os.environ['FERNET_KEY'], algorithm='HS256')
 
    return token
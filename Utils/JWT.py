from typing import Optional
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Cookie, Depends, status, HTTPException,Response
from sqlalchemy import true
from sqlalchemy.orm import Session
from config import settings
from DB.db_setup import get_db
from pydantic_schemas import pydantic_Users
from config import settings

ACCESS_KEY = settings.access_key
REFRESH_KEY = settings.refresh_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE = settings.access_expire
REFRESH_TOKEN_EXPIRE = settings.refresh_expire

def create_tokens(data: dict,KEY:str,ALGO:str,EXPIRE:str):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRE)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, KEY, algorithm=ALGO)

    return encoded_jwt

def verify_token(token: str,SECRET_KEY:str ,ALGO:str):

    try:
        User = jwt.decode(token, SECRET_KEY, algorithms=ALGO)
        if User is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return User

#get user middleware
def get_current_user(response:Response,ACCESS_TOKEN: Optional[str] = Cookie(None),REFRESH_TOKEN: Optional[str] = Cookie(None)):
    if(REFRESH_TOKEN==None):
        return None
    if(ACCESS_TOKEN==None):
        decoded= verify_token(REFRESH_TOKEN,REFRESH_KEY,ALGORITHM)
        ACCESS_TOKEN=create_tokens(decoded,ACCESS_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE)
        REFRESH_TOKEN=create_tokens(decoded,REFRESH_KEY,ALGORITHM,REFRESH_TOKEN_EXPIRE)
        response.set_cookie(key="ACCESS_TOKEN",value=ACCESS_TOKEN,max_age=60000,httponly=true)
        response.set_cookie(key="REFRESH_TOKEN",value=REFRESH_TOKEN,max_age=900000,httponly=true)
        return decoded
    decoded= verify_token(ACCESS_TOKEN,ACCESS_KEY,ALGORITHM)
    ACCESS_TOKEN=create_tokens(decoded,ACCESS_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE)
    REFRESH_TOKEN=create_tokens(decoded,REFRESH_KEY,ALGORITHM,REFRESH_TOKEN_EXPIRE)
    response.set_cookie(key="ACCESS_TOKEN",value=ACCESS_TOKEN,max_age=300000,httponly=true)
    response.set_cookie(key="REFRESH_TOKEN",value=REFRESH_TOKEN,max_age=900000,httponly=true)   
    return decoded
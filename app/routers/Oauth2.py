import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from typing import Optional

from .. import schemas, database, models
from ..config import settings

from fastapi.security import OAuth2PasswordBearer

#this variable is going to be used to extract the token from the request header when the user makes a request to a protected route that requires authentication. 
# The tokenUrl parameter specifies the endpoint where the user can obtain a token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Secret key for encoding and decoding JWT tokens
# algorithm used for encoding and decoding JWT tokens
# Expiration time for the JWT tokens (e.g., 30 minutes)
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    # Create a copy of the data to avoid modifying the original data
    to_encode = data.copy()
    
    # Add an expiration time to the token
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Encode the data into a JWT token using the secret key and algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):

    try:
        # Decode the token using the secret key and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Extract the user id from the payload
        id: int = payload.get("user_id")
        
        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=id)
    except InvalidTokenError:
        raise credentials_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                        detail=f"Could not validate credentials", 
                                        headers={"WWW-Authenticate": "Bearer"},)
    
    token_data = verify_access_token(token, credentials_exception)
    db_user = db.query(models.User).filter(models.User.id == token_data.id).first()
    return db_user
    # return verify_access_token(token, credentials_exception)
    
    # user = db.query(models.User).filter(models.User.id == token_data.id).first()
    
    # return user
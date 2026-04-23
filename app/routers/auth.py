from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db


from .. import schemas, models, utils
from . import Oauth2


router = APIRouter(
    tags=["Authentication"])

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    # check if the user exists in the database using their email, if they do, then we can verify their password and return a token if the credentials are valid.
    # If the credentials are invalid, we can return an error message.
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    # If the credentials are valid, we can generate a token (e.g., JWT) and return it to the client for authentication in subsequent requests.  
    # create and return access token (Here you can create the payload and put whatever you want inside the token, 
    # but usually we put the user id inside the token so that we can identify the user in subsequent requests using the token)
    access_token = Oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}

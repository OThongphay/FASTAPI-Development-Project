from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags = ['Authentication'])

#Method for user login
@router.post("/login", response_model = schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    #Query searches the users table for the first matching email
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    #Status exception if a user isn't found
    if not user:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Invalid Credentials")

    #Status exception if the passwords don't match the ones in the database
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Invalid Credentials")

    #Creates an access token encoding the user id
    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
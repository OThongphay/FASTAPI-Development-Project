from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl ='login')

#SECRET_KEY
#Algorithm
#Expiration time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

#Model to create an access token function
def create_access_token(data: dict):

    #Copies the data to be used for encoding
    to_encode = data.copy()

    #Takes the time starting now and expires it the set number of minutes from now
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    #Applies the data encoded with expiry time, secret key, and algorithm to the variable and uses jwt to encode
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)

    return encoded_jwt

#Model to verify the access token function
def verify_access_token(token: str, credentials_exception):

    try:

        #Access the jwt library to decode the token, secret key, and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])

        #Gets the user_id in the payload and puts in id variable as a string
        id:str = payload.get("user_id")

        #If there is no id a credential_exception is raised
        if id is None:
            raise credentials_exception

        #Validate if it matches the schema data
        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise credentials_exception

    return token_data

#Method to see if user is curretly logged in, ensuring they are accessing a resource they need to be currently logges in
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):

    #Credentials exception if they are not authenticated
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = f"Could not validate credentials", headers = {"WWW=Authenticate": "Bearer"})

    #Sets token to the verify_access_token model to check if their token is valid
    token = verify_access_token(token, credentials_exception)

    #Queries the database to find a user id that matches the token id
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
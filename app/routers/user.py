from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(prefix = "/users", tags = ['Users'])

#Path to create a user
@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    #Hashes the password - user.password
    hashed_password = utils.hash(user.password)

    #Sets user password to new hashed password
    user.password = hashed_password

    #Unpacks the user.dict to get values and then sends a query to the db to send the data
    new_user = models.User(**user.dict())

    #Adds new user to db
    db.add(new_user)

    #Commits new user to db
    db.commit()

    #Retrieves the newly commited user and reinsert the values back inside the variable
    db.refresh(new_user)

    return new_user

#Path to get to get a user with a certain id
@router.get("/{id}", response_model = schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):

    #Searches for a specific user based on id specified
    user = db.query(models.User).filter(models.User.id == id).first()

    #Returns 404 if user not found
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with id: {id} does not exist")

    return user
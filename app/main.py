from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

#Model to create a database table
#models.Base.metadata.create_all(bind = engine)

#API reference
app = FastAPI()

#Parameters to define from WHERE a person can access the API from
origins = ['*']

#Cors middleware that allows people from other domains to talk with FASTAPI 
app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)


#Ensures the path to the post folder is included 
app.include_router(post.router)

#Ensures the path to the user folder is included 
app.include_router(user.router)

#Ensures path to auth folder is included 
app.include_router(auth.router)

#Ensures path to vote folder is included 
app.include_router(vote.router)

# Method to the path to "/"
@app.get("/")
async def root():
    return {"message": "Welcome to my API:D"}

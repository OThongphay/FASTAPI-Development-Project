from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix = "/posts", tags = ['Posts'])


# Method to path to the "/post" getting all posts, executing the SQL statmet to fetch all posts
@router.get("/", response_model = List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    #Raw SQL command to generate all posts
    #cursor.execute(""" SELECT * FROM posts """)
    #posts = cursor.fetchall()
    
    #Taps into the databse object to grab a query for all posts or a specific post within the parameters
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    #Database query that joins the post and votes table via a left outer join and counts the votes for each post and labels the column as votes with the filter from the previous commented line of code
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts

# Method to create a post with "/createposts"
@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    #Raw SQL command to generate one post and sanitizes it to prevent SQL injections
    #cursor.execute("""INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #Commits the post to the database
    #conn.commit()

    #Unpacks the post.dict to get values and then sends a query to the db to send the data
    new_post = models.Post(owner_id = current_user.id, **post.dict())

    #Adds new post to db
    db.add(new_post)

    #Commits new post to db
    db.commit()

    #Retrieves the newly commited post and reinsert the values back inside the variable
    db.refresh(new_post)

    return new_post

#It extracts the id to find a specific post 
@router.get("/{id}", response_model = schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db)):

    #Raw sql command to get a certain post using the id
    #cursor.execute("""SELECT * FROM posts WHERE id = %s """, (id,))
    #post =cursor.fetchone()

    #Query for the database that filters the posts by id til a matching id is found
    #post = db.query(models.Post).filter(models.Post.id == id).first()

    #Database query that joins the post and votes table via a left outer join and counts the votes for each post and labels the column as votes with the filter from the previous commented line of code
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()

    #If a post isnt fount it raises the 404 exception 
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} was not found")
    return post

#Method to deleting the post
@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    #Raw sql command that deletes a certain post based on the id specified
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (id,))
    #deleted_post = cursor.fetchone()
    #conn.commit()

    #Retrieves the post by ID
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()

    #If statement to catch an exception and send an 404 error
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} was not found")

    #If statement to chech if the owner is trying to delete their own post, if not there is an exception 403 error
    if post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action")

    #Deletes the post and commits changes
    post_query.delete(synchronize_session = False)
    db.commit()
    
    return Response(status_code = status.HTTP_204_NO_CONTENT)

#Method to updating a post with a specific id
@router.put("/{id}", response_model = schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    #SQL command to update a specific post's title, content, pubished via it's id
    #cursor.execute("""update POSTS set title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, (id,)))
    #updated_post = cursor.fetchone()
    #conn.commit()

    #Query to find post with id
    post_query = db.query(models.Post).filter(models.Post.id == id)

    #Grabs that first post with the id
    post = post_query.first()
    
    #If statement to catch an exception
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} was not found")
    
    #If statement to chech if the owner is trying to update their own post, if not there is an exception 403 error
    if post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action")

    #Unpacks the fields in the dict and updates them in the db along with committing
    post_query.update(updated_post.dict(), synchronize_session = False)
    db.commit()
    
    return post_query.first()
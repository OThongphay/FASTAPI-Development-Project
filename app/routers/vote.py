from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(prefix = "/vote", tags = ['Vote'])

#Router Path for voting on posts
@router.post("/", status_code = status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    #Query for a post based off the id
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    #Exception if the post does not exist
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id {vote.post_id} does not exist")
        
    #Checks if there is already a vote for this post ID
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    #Logic for if vote direction is 1
    if (vote.dir == 1):

        #If they found that they already voted on specified post
        if found_vote:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = f"user {current_user.id} has already voted on post {vote.post_id}")
        
        #Creates a new vote
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        
        #Adds and commits the new vote to the database
        db.add(new_vote)
        db.commit()
        
        return {"message": "Successfully added vote"}

    #Logic if the vote direction is 0    
    else:

        #If they did not find a vote
        if not found_vote:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Vote does not exist")
        
        #Deletes the vote and commits it to the database
        vote_query.delete(synchronize_session = False)
        db.commit()

        return {"message": "Successfully deleted vote"}
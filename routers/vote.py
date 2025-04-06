from fastapi import Depends, FastAPI  , Response , status , HTTPException , APIRouter 
import schemas
from database import get_db
from sqlalchemy.orm import Session
import models
from oauth import get_current_user 
from sqlalchemy import  func
from utils import to_dict_list
from typing import List
import logging

logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/vote" , 
    tags= ["Vote"] 

)

@router.post('/' , status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote ,  db:Session = Depends(get_db)  , current_user:int= Depends(get_current_user)):
    vote_query = db.query(models.Vote).filter(models.Vote.post_id==vote.id , models.Vote.user_id == current_user.id)
    found_vote=vote_query.first()
    
    # Check is post if there 
    post_id = vote.id
    post = db.query(models.Post).filter(models.Post.id==post_id).first()

    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Post not found")
    
    
    if vote.dir == 1 :
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT , detail=f"User has already voted")
        new_vote = models.Vote( user_id=current_user.id , post_id=vote.id )
        db.add(new_vote)
        db.commit()
        return {"message":"sucessfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"sucessfully deleted vote"}
    


@router.get('/get_votes'  , response_model=List[schemas.PostOut] )
def get_votes(db:Session = Depends(get_db)):
    logger.info("Inside get votes")

    
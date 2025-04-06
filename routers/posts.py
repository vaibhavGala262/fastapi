
from fastapi import Depends, FastAPI  , Response , status , HTTPException , APIRouter 
from sqlalchemy.orm import Session
from database import get_db
import models , schemas 
from typing import List
from oauth import get_current_user , verify_access_token
from typing import Optional
from sqlalchemy import func
router = APIRouter(
    prefix='/posts',
    tags=["Posts"]
    
)

@router.get('/myposts'  )
def get_myposts(db: Session=Depends(get_db) , current_user:int= Depends(get_current_user)):
    posts = db.query(models.Post , func.count(models.Vote.post_id).label("votes")).join(
        models.Vote , models.Vote.post_id == models.Post.id ,isouter= True
    ).filter(models.Post.owner_id== current_user.id).group_by(models.Post.id).all()

    response = []
    for post, votes in posts:
        # First convert the owner using model_validate
        post_model = schemas.PostResponse.model_validate(post)
        # Create the PostOut object and add to response
        post_out = schemas.PostOut(Post=post_model, votes=votes)
        response.append(post_out)
    
    if not response: 
        return {'detail' : f'no posts found'}
    return {'posts' : response}

@router.get('/' ,  response_model=List[schemas.PostOut])
def get_posts(db: Session=Depends(get_db) , current_user:int= Depends(get_current_user) , limit : int=10 , skip:int=0  , search : Optional[str]=""):
    # fetching post using query parameter but this iss not optimal as we also need like on the post 
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit=limit).offset(offset=skip).all()

    results = (
    db.query(
        models.Post,
        func.count(models.Vote.post_id).label("votes")
    )
    .join(
        models.Vote,
        models.Vote.post_id == models.Post.id,
        isouter=True
    )
    .filter(models.Post.title.contains(search))
    .group_by(models.Post.id)
    .limit(limit)
    .offset(skip)
    .all()
)
    response = []
    for post, votes in results:
        # First convert the owner using model_validate
        post_model = schemas.PostResponse.model_validate(post)
        # Create the PostOut object and add to response
        post_out = schemas.PostOut(Post=post_model, votes=votes)
        response.append(post_out)

    
    return response
    
    
    


@router.get('/{id}' , response_model=List[schemas.PostOut])
def get_post(id : int  , response : Response , db: Session=Depends(get_db), current_user:int= Depends(get_current_user) ):
    
    results = db.query(models.Post , func.count(models.Vote.post_id).label("votes")).join(
        models.Vote , models.Vote.post_id == models.Post.id ,isouter= True
    ).filter(models.Post.id==id).group_by(models.Post.id).all()

    response = []
    for post, votes in results:
        post_model = schemas.PostResponse.model_validate(post)
        post_out = schemas.PostOut(Post=post_model, votes=votes)
        response.append(post_out)


    if not response :
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail = f"post with id {id} not found")  
    # set http codde and detail as json

    return response


@router.post('/' ,   status_code =status.HTTP_201_CREATED , response_model=schemas.PostResponse)
def create_names(new_post :schemas.CreatePost  , db: Session=Depends(get_db), current_user:int= Depends(get_current_user)):
    
    post= models.Post(owner_id =  current_user.id , **new_post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)  # post added to database commited then refresh gets post its value
    
    return post


@router.delete('/{id}' , status_code=status.HTTP_204_NO_CONTENT  )
def delete_post(id : int , db: Session=Depends(get_db) , current_user:int= Depends(get_current_user)):

    post= db.query(models.Post).filter(models.Post.id== id)
    if not post.first() : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f'post with id {id} not found')
    
    if post.first().owner_id != current_user.id :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail=f'not allowed to delete post with id {id}')
    
    
    print(post)
    post.delete(synchronize_session=False)
    db.commit()
    return {'detail' : f'post with id {id} deleted'}

@router.put('/{id}'   , status_code=status.HTTP_202_ACCEPTED     )
def update_post(id :int , updated_post:schemas.UpdatePost  , db: Session=Depends(get_db) , current_user:int= Depends(get_current_user)):
    post_query= db.query(models.Post).filter(models.Post.id== id)
    
    if not post_query.first() :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f'post with id {id} not found')
    print(post_query.first().owner_id)
    print(current_user.id)

    if post_query.first().owner_id != current_user.id :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail=f'not allowed to update post with id {id}')
    

    post_query.update({ **updated_post.dict( ) }, synchronize_session=False)
    db.commit()

    return {'detail' : f'post with id {id} updated'}






from fastapi import Depends, FastAPI  , Response , status , HTTPException , APIRouter 
from sqlalchemy.orm import Session
from database import get_db
import models , schemas 
from typing import List
from utils import hash
from oauth import create_access_token , verify_access_token , get_current_user


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
@router.post('/' , status_code=status.HTTP_201_CREATED , response_model=schemas.UserResponse)
def create_users(new_user: schemas.CreateUser , db: Session=Depends(get_db) ):
    
    new_user.password= hash(new_user.password)
    user= models.User(**new_user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)  # post added to data
    return user

@router.get('/' , status_code=status.HTTP_200_OK)
def get_users( db: Session=Depends(get_db) , current_user:int= Depends(get_current_user)):
    
    users= db.query(models.User).all()
    return users

@router.get('/{id}' , response_model=schemas.UserResponse) 
def get_user(id: int , db: Session=Depends(get_db) ,current_user:int= Depends(get_current_user)):
    user_query= db.query(models.User).filter(models.User.id== id)
    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f'user with id {id} is not present')
    return user_query.first()

from  datetime import datetime
from pydantic import BaseModel, ConfigDict,SkipValidation , EmailStr ,conint
from typing import Optional 


class PostBase(BaseModel):
    title: str
    content : str  
    published : bool = True  # optional field 
    rating : Optional[int] = None # optional field

class CreatePost(PostBase):
    pass


class UpdatePost(PostBase):
    
    pass
    
class UserResponse(BaseModel):
    id: int 
    email: EmailStr
    created_at: datetime
    model_config = {
        "from_attributes": True
    }


class PostResponse(BaseModel):
    id:int
    title :str
    content:str 
    published:bool
    rating: Optional[int]= None
    created_at: datetime
    owner : UserResponse 
    
    model_config = {
        "from_attributes": True
    }
    
class PostOut(BaseModel):
    Post: PostResponse
    votes : int
    model_config = {
        "from_attributes": True
    }
    
    

class CreateUser(BaseModel):
    email: EmailStr
    password:str
    



class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    id: int 
    dir : conint(le=1)






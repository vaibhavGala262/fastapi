
from sqlalchemy import TIMESTAMP, Column , String ,Boolean, Integer, text , ForeignKey 
from sqlalchemy.orm import relationship
from database import Base



class Post(Base):
    __tablename__ = 'posts'

    id =Column(Integer , primary_key=True , index= True)
    title= Column(String , nullable= False)
    content = Column(String , nullable=False)
    published = Column(Boolean , server_default='True' , nullable=False)
    rating = Column(Integer , nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False  , server_default=text('now()'))
    owner_id  = Column(Integer ,ForeignKey("users.id",  ondelete="CASCADE" , onupdate="CASCADE") , nullable=False)
    owner = relationship("User")


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer , primary_key=True , index= True)
    email=Column(String , nullable=False , unique=True)
    password = Column(String , nullable=False)
    created_at= Column(TIMESTAMP(timezone=True), nullable=False  , server_default=text('now()'))



class Vote(Base):
    __tablename__ = 'votes'
    user_id = Column(Integer , ForeignKey("users.id"  , ondelete="CASCADE" , onupdate="CASCADE") , primary_key=True)
    post_id = Column(Integer  , ForeignKey("posts.id" , ondelete="CASCADE" , onupdate="CASCADE" ) , primary_key=True)
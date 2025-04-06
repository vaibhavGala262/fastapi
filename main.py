from fastapi import Depends, FastAPI  , Response , status , HTTPException 
import uvicorn
import models
from database import engine , get_db
from routers import posts , users , auth , vote
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
app = FastAPI()

origins= [
    "https://www.google.com", 
    "https://www.youtube.com"
]

#models.Base.metadata.create_all(bind=engine)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "localhost",
        "127.0.0.1",
        "vaibhavs-fastapi.onrender.com"
    ]
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)



@app.get('/')
def home():
    return 'Hello'


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=9000, reload=True)




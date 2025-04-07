from pydantic_settings import BaseSettings
from dotenv import load_dotenv


import os

load_dotenv()

DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOSTNAME = os.getenv("DATABASE_HOSTNAME")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")


class Settings(BaseSettings):
    database_hostname: str
    database_port: str 
    database_password: str 
    database_name: str
    database_username:  str
    secret_key:str 
    algorithm: str
    access_token_expire_minutes:int 

    class Config:
        env_file = ".env"

settings = Settings()


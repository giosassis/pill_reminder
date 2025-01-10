from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str
    USER_NAME: str

    class Config:
        env_file = "../.env"
        extra = "forbid" 

class SESConfig(BaseSettings):
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str
    SENDER_EMAIL: str

    class Config:
        env_file = "../.env"  
        extra = "forbid" 

settings = Settings() 
ses_config = SESConfig()


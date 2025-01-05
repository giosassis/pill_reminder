import logging
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv() 

class Settings(BaseSettings):
    DATABASE_URL: str

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
        extra = "allow"

# Instanciando as configurações separadas
settings = Settings() 
ses_config = SESConfig()  

# Log para verificar as variáveis
logging.info(ses_config.AWS_ACCESS_KEY_ID)
logging.info(ses_config.AWS_SECRET_ACCESS_KEY)
logging.info(ses_config.AWS_REGION)
logging.info(ses_config.SENDER_EMAIL)

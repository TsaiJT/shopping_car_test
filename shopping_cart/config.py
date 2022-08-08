# built-in
import os
import urllib.parse

# 3rd
from pydantic import BaseSettings
from dotenv import load_dotenv, find_dotenv



class Settings(BaseSettings):
    load_dotenv(find_dotenv())

    PORT = 8000

    # postgres db
    POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_CERT = os.getenv("POSTGRES_CERT")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(POSTGRES_USER,
                                                                urllib.parse.quote_plus(POSTGRES_CERT.encode("utf-8")),
                                                                POSTGRES_SERVER,
                                                                POSTGRES_PORT,
                                                                POSTGRES_DB)


    # jwt setting
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY")
    ALGORITHM = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days

# init settings obj
settings = Settings()


# my_project/config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Loads .env from project root

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{os.getenv('username')}:{os.getenv('password')}@{os.getenv('host')}/{os.getenv('dbname')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
dbname = os.getenv("DB_NAME")
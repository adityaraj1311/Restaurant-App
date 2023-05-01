from os import environ, path, getcwd #path generalizes the path, getcwd returns the path of the folder we're working on 
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv(path.join(getcwd(), ".env"))

SECRET_KEY = environ.get('SECRET_KEY')

#create a db object
db = SQLAlchemy()
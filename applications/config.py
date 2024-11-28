from dotenv import load_dotenv
import os
load_dotenv()


class Config():
    SQL_ALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    DEBUG = True
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = os.getenv('SALT')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'

    

    WTF_CSRF_ENABLED = False
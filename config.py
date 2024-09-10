# config.py
class Config:
    TESTING = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///todo.db'  # replace with your production DB
    # other config variables

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_todo.db'  # use a separate test database
    DEBUG = False
    # other config variables

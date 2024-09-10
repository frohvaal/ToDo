# config.py
class Config:
    TESTING = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'  # replace with your production DB
    # other config variables

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'  # use a separate test database
    DEBUG = False
    # other config variables

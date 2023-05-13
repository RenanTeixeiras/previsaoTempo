import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'FUCKU'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///banco.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False







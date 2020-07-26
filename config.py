import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

ENV = 'dev';

if ENV != 'dev':
    # Enable debug mode.
    DEBUG = True
    # Connect to the database
    # TODO_DONE IMPLEMENT DATABASE URL
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:0008@localhost:5432/fyyur'
else:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgres://pntdfomabqppgb:300f71e6521c3bf76a57e0c5a083b7baf41a014acc06186590ffcd018d215a3f@ec2-54-234-28-165.compute-1.amazonaws.com:5432/d8cjoh1e4c4gdg'

SQLALCHEMY_TRACK_MODIFICATIONS = False

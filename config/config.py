import json
import logging
import os
logging.basicConfig(level=logging.INFO)
basedir = os.path.abspath(os.path.dirname(__file__))
def configs():
    with open('./config/config.json', 'r') as f:
        config = json.load(f)
    logging.info(config)
    f.close()
    return config

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, '../app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'file_csv'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'





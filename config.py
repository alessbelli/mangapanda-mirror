import os

DEFAULT_SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/mangapanda-mirror-test'


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or DEFAULT_SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
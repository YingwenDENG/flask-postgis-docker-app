import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")    # get the URI from DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
#     STATIC_FOLDER = f"{os.getenv('APP_FOLDER')}/project/static"
#     TEMPLATES_FOLDER = f"{os.getenv('APP_FOLDER')}/project/templates"
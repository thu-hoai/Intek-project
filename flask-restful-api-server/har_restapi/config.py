"""A configuration of the application"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Define the connection we need to connect to database
DATABASE_TYPE = 'postgresql'
DATABASE_CONNECTOR = 'psycopg2'
USERNAME = 'postgres'
PASSWORD = 'postgres'
HOST = '127.0.0.1'
PORT = '5432'
DATABASE_NAME = 'heritage'
# the place where we store the uploaded files
UPLOADED_FOLDER = '~/var/lib/har/photo'


class Config:
    """A configuration Class"""
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    # Ignore the wanning that the app takes a lot of system resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Define connection string
    SQLALCHEMY_DATABASE_URI = \
        f'{DATABASE_TYPE}+{DATABASE_CONNECTOR}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}'
    # TRAP_HTTP_EXCEPTIONS = True
    UPLOAD_FOLDER = os.path.expanduser(UPLOADED_FOLDER)

import os


class Local:
    # debug Mode : True/False
    DEBUG = True

    # root path of server
    ROOT_DIR = os.path.dirname(os.path.dirname(__file__))

    # DATABASE CREDENTIALS HERE
    DATABASE_ENDPOINT = 'localhost'
    DATABASE_USERNAME = 'postgres'
    DATABASE_PASSWORD = 'postgres'
    DATABASE_PORT = 5432
    DATABASE_NAME = 'todo_app'

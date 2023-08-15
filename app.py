"""
Main file to start the project
"""
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from todo_app.data_access.sql_alchemy import register_sqlalchemy
from todo_app.todo_resources.resources import TodoResource, TodoCreateResource, TodoDecryptResource
from todo_app.user_resources.resources import UserResource, UserCreate, UserLoginResource
from todo_app.env_configs.development import Local
from todo_app.encryption import encrypt_data, encrypt_data


def create_app(config_object):
    """
    Basic configurations for the project
    :param config_object:
    :return:
    """
    flask_app = Flask(__name__)
    api = Api(flask_app)
    JWTManager(flask_app)

    flask_app.config.from_object(config_object)
    initialize_sqlalchemy(flask_app)
    api.add_resource(TodoResource, '/todo/<int:id>/')
    api.add_resource(TodoDecryptResource, '/decrypt/')
    api.add_resource(TodoCreateResource, '/todo/')
    api.add_resource(UserResource, '/user/<int:id>/')
    api.add_resource(UserCreate, '/user/')
    api.add_resource(UserLoginResource, '/login/')
    return flask_app


def initialize_sqlalchemy(flask_app):
    """
    initializing the sqlachemy to uese ORM
    :param flask_app:
    :return:
    """
    register_sqlalchemy(flask_app)


app = create_app(Local)  # Local is environment file

if __name__ == '__main__':
    app.run(debug=True)

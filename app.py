from flask import Flask
from flask_restful import Api
from todo_app.data_access.sql_alchemy import register_sqlalchemy
from todo_app.todo_resources.resources import TodoResource, TodoCreateResource
from todo_app.user_resources.resources import UserResource, UserCreate, UserLoginResource
from todo_app.env_configs.development import Local
from flask_jwt_extended import JWTManager


def create_app(config_object):
    flask_app = Flask(__name__)
    api = Api(flask_app)
    jwt = JWTManager(flask_app)

    flask_app.config.from_object(config_object)
    initialize_sqlalchemy(flask_app)
    api.add_resource(TodoResource, '/todo/<int:id>/')
    api.add_resource(TodoCreateResource, '/todo/')
    api.add_resource(UserResource, '/user/<int:id>/')
    api.add_resource(UserCreate, '/user/')
    api.add_resource(UserLoginResource, '/login/')
    return flask_app


def initialize_sqlalchemy(flask_app):
    register_sqlalchemy(flask_app)


env = Local
app = create_app(env)

if __name__ == '__main__':
    app.run(debug=True)

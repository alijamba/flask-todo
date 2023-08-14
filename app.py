from flask import Flask
from todo_app.data_access.sql_alchemy import register_sqlalchemy
from todo_app.env_configs.development import Local


def create_app(config_object):
    flask_app = Flask(__name__)

    flask_app.config.from_object(config_object)
    initialize_sqlalchemy(flask_app)
    return flask_app


def initialize_sqlalchemy(flask_app):
    register_sqlalchemy(flask_app)


env = Local
app = create_app(env)

if __name__ == '__main__':
    app.run(debug=True)

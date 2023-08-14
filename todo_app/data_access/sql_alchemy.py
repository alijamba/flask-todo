import urllib
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData


convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)


def register_sqlalchemy(app):
    dialect = 'postgresql'
    username = app.config.get('DATABASE_USERNAME')  # postgres
    password = urllib.parse.quote(app.config.get('DATABASE_PASSWORD'))      # postgres
    host = app.config.get('DATABASE_ENDPOINT')      # localhost
    port = app.config.get('DATABASE_PORT')          # 5432
    db_name = app.config.get('DATABASE_NAME')       # todo_app

    DB_URL = f"{dialect}://{username}:{password}@{host}:{port}/{db_name}"

    app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    migrate = Migrate(app, db)
    # NOTE: Use code below if needed to update field type
    # migrate = Migrate(app, db, compare_type=True)
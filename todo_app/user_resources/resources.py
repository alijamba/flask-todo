import datetime
import jwt
import uuid
from flask_restful import Resource, reqparse
from todo_app.data_access.sql_alchemy import db
from todo_app.data_access.models.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app as app
from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True, help='Title is required')
parser.add_argument('password', type=str, required=True, help='Title is required')


class UserResource(Resource):
    @jwt_required()
    def get(self, id):
        user = User.query.filter_by(uuid=id).first()
        if not user:
            return {'message': 'User not found'}, 404
        return {'title': user.id, 'description': user.name}, 200

    @jwt_required()
    def delete(self, id):
        user = User.query.filter_by(uuid=id).first()
        if not user:
            return {'message': 'User not found'}, 404
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully'}, 204


class UserCreate(Resource):
    @jwt_required()
    def get(self):
        user = User.query.all()
        res = []
        for val in user:
            res.append(
                {"id": val.id,
                 "username": val.name,
                 "created_at": str(val.created_at),
                 "updated_at": str(val.updated_at)
                 }
            )
        return jsonify(res)

    def post(self):
        data = parser.parse_args()
        name = data['username']
        password = data['password']
        hashed_pass = generate_password_hash(password, method="sha256")
        user_obj = User()
        user_obj.name = name
        user_obj.password = hashed_pass
        user_obj.uuid = str(uuid.uuid4())
        user_obj.created_at = datetime.datetime.now()
        user_obj.updated_at = datetime.datetime.now()
        db.session.add(user_obj)
        db.session.commit()
        return ['created'], 201


class UserLoginResource(Resource):

    def post(self):
        data = parser.parse_args()
        if "username" not in data or "password" not in data:
            return {"message": "not verified"}, 401
        if not data["username"] or not data["password"]:
            return {"message": "not verified"}, 401

        username = data["username"]
        password = data["password"]

        user_obj = User.query.filter_by(name=username).first()
        if not user_obj:
            return {"message": "not verified"}, 401

        if check_password_hash(user_obj.password, password):
            # jwt_token = jwt.encode({"uuid": user_obj.uuid, "exp": datetime.datetime.now() + datetime.timedelta(hours=10)}, app.config.get('SECRET_KEY'))
            jwt_token = create_access_token(identity={"id":user_obj.uuid})
            return {"token": (jwt_token)}, 200

        return {"message": "not verified"}, 401






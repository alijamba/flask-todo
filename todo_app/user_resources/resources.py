"""
this contains the Restful methods to create, update, delete and login users
"""
import datetime
import uuid
from flask_restful import Resource, reqparse
from todo_app.data_access.sql_alchemy import db
from todo_app.data_access.models.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, make_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True, help='Title is required')
parser.add_argument('password', type=str, required=True, help='Title is required')
parser.add_argument('admin', type=bool, required=False)


class UserResource(Resource):
    """
    This is user class to make APIs
    """
    @jwt_required()
    def get(self):
        """
        To get particular user
        :return: json
        """
        user = User.query.filter_by(uuid=get_jwt_identity()['uuid']).first()
        if not user:
            return make_response('User not found', 404)
        return jsonify({'title': user.uuid, 'description': user.name})

    @jwt_required()
    def delete(self, user_id_to_be_deleted):
        """
        To delete a particular user
        :param user_id_to_be_deleted: str
        :return: json
        """
        logged_in_user = User.query.filter_by(uuid=get_jwt_identity()['uuid']).first()
        if logged_in_user and not logged_in_user.admin:
            return make_response("not admin. permission denied", 401)

        user = User.query.filter_by(uuid=user_id_to_be_deleted).first()
        if not user:
            return make_response('User not found', 404)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'})


class UserCreate(Resource):
    """
    this class contains end point to delete create new user
    """
    @jwt_required()
    def get(self):
        """
        To get all users
        :return:
        """
        logged_in_user = User.query.filter_by(uuid=get_jwt_identity()['uuid']).first()
        if logged_in_user and not logged_in_user.admin:
            return make_response("not admin. permission denied", 401)

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
        """
        To create new user
        :param: username: str
                password: str
                admin: bool
        :return:
        """
        data = parser.parse_args()
        name = data['username']
        password = data['password']
        hashed_pass = generate_password_hash(password, method="sha256")
        user_obj = User()
        user_obj.name = name
        if 'admin' in data and data['admin']:
            user_obj.admin = data['admin']
        user_obj.password = hashed_pass
        user_obj.uuid = str(uuid.uuid4())
        user_obj.created_at = datetime.datetime.now()
        user_obj.updated_at = datetime.datetime.now()
        db.session.add(user_obj)
        db.session.commit()
        return jsonify({"msg": "successfully created"})


class UserLoginResource(Resource):
    """
    Login
    """
    def post(self):
        """
        To get token against particular user
        :param: username: str
                password: str
        :return:
        """
        data = parser.parse_args()
        if "username" not in data or "password" not in data:
            return make_response("username and password required", 401)
        if not data["username"] or not data["password"]:
            return make_response("username and password required", 401)

        username = data["username"]
        password = data["password"]

        user_obj = User.query.filter_by(name=username).first()
        if not user_obj:
            return make_response("user not found against username", 401)

        if check_password_hash(user_obj.password, password):
            jwt_token = create_access_token(identity={"uuid": user_obj.uuid})
            return jsonify({"token": jwt_token})

        return make_response("invalid token", 401)

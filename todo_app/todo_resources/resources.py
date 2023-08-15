"""
This file contains all the Restful methods for TODO task.
"""
import datetime
import ast
from flask_restful import Resource, reqparse
from todo_app.data_access.sql_alchemy import db
from todo_app.data_access.models.models import Todo
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, make_response
from todo_app.encryption.encrypt_data import generate_key, encrypt_data, decrypt_data

encryption_key = generate_key()

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, required=False)
parser.add_argument('description', type=str, required=False)
parser.add_argument('completed', type=bool, required=False)
parser.add_argument('encrypted_data', type=str, required=False)


class TodoResource(Resource):
    """
    This class contains GET, PUT, and DELETE methods
    for the todo
    """

    @jwt_required()
    def get(self, id):
        """
        To get single todo against id
        :param id: int
        :return: json
        """
        todo = Todo.query.filter_by(id=id, user_id=get_jwt_identity()['uuid']).first()
        if not todo:
            return make_response('Not found', 401)
        encrypted_data = encrypt_data(encryption_key, {'title': todo.title,
                                                       'description': todo.description,
                                                       'created_at': todo.created_at,
                                                       'updated_at': todo.updated_at})
        return jsonify({"encrypted_data": str(encrypted_data)})

    @jwt_required()
    def put(self, id):
        """
        To update the todo against id
        :param id: int
                title: str
                description: str
        :return: json
        """
        data = parser.parse_args()
        todo = Todo.query.filter_by(id=id, user_id=get_jwt_identity()['uuid']).first()
        if not todo:
            return make_response('Not found', 401)
        if 'title' in data and data['title']:
            todo.title = data['title']
        if 'description' in data and data['description']:
            todo.description = data['description']
        if 'completed' in data and data['completed']:
            todo.completed = data['completed']
        db.session.commit()
        return jsonify({'msg': 'Updated successfully'})

    @jwt_required()
    def delete(self, id):
        """
        TO delete the todo against id
        :param id: int
        :return: json
        """
        todo = Todo.query.filter_by(id=id, user_id=get_jwt_identity()['uuid']).first()
        if not todo:
            return make_response('Not found')
        db.session.delete(todo)
        db.session.commit()
        return jsonify({'msg': 'Todo deleted successfully'})


class TodoCreateResource(Resource):
    """
    This class Contains GET and POST methods
    """

    @jwt_required()
    def get(self):
        """
        To get all todos against particular user
        :return: json
        """
        todo = Todo.query.filter_by(user_id=get_jwt_identity()['uuid']).all()
        res = []
        for val in todo:
            res.append(
                {
                    "id": val.id,
                    "title": val.title,
                    "description": val.description,
                    "completed": val.completed,
                    "user_id": val.user_id,
                    "created_at": str(val.created_at),
                    "updated_at": str(val.updated_at)
                }
            )
        encrypted_data = encrypt_data(encryption_key, res)
        return jsonify({"encrypted_data": str(encrypted_data)})

    @jwt_required()
    def post(self):
        """
        TO create new todo against one user
        :return: json
        """
        data = parser.parse_args()
        title = data['title']
        description = data['description']
        todo_obj = Todo()
        todo_obj.title = title
        todo_obj.description = description
        todo_obj.user_id = get_jwt_identity()['uuid']
        todo_obj.created_at = datetime.datetime.now()
        todo_obj.updated_at = datetime.datetime.now()
        db.session.add(todo_obj)
        db.session.commit()
        return jsonify({"msg": "successfully created!"})


class TodoDecryptResource(Resource):
    """
    To decrypt the data
    """

    @jwt_required()
    def post(self):
        """
        To decrypt the response use this POST end point
        :param: data: str
        :return: json
        """
        data = parser.parse_args()
        encrypted_data = data["encrypted_data"]
        encrypted_data = ast.literal_eval(encrypted_data)
        decrypted_data = decrypt_data(encryption_key, encrypted_data)
        return jsonify(decrypted_data)


import datetime
from flask_restful import Resource, reqparse
from todo_app.data_access.sql_alchemy import db
from todo_app.data_access.models.models import Todo
from flask_jwt_extended import jwt_required
from flask import jsonify, make_response

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, required=True, help='Title is required')
parser.add_argument('description', type=str, required=False)


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
        todo = Todo.query.get(id)
        if not todo:
            return make_response('Todo not found', 401)
        return jsonify({'title': todo.title, 'description': todo.description})

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
        todo = Todo.query.get(id)
        if not todo:
            return make_response('Todo not found', 401)
        todo.title = data['title']
        todo.description = data['description']
        db.session.commit()
        return jsonify({'message': 'Todo updated successfully'})

    @jwt_required()
    def delete(self, id):
        """
        TO delete the todo against id
        :param id: int
        :return: json
        """
        todo = Todo.query.get(id)
        if not todo:
            return make_response('Todo not found')
        db.session.delete(todo)
        db.session.commit()
        return jsonify({'message': 'Todo deleted successfully'})


class TodoCreateResource(Resource):
    """
    This class Contains GET and POST methods
    """
    @jwt_required()
    def get(self, id):
        """
        To get all todos against particular user
        :return: json
        """
        todo = Todo.query.filter_by(user_id=id).all()
        res = []
        for val in todo:
            res.append(
                {"title": val.title,
                 "description": val.description,
                 "created_at": str(val.created_at),
                 "updated_at": str(val.updated_at)
                 }
            )
        return jsonify(res)

    @jwt_required()
    def post(self):
        """
        TO create new todo against one user
        :return:
        """
        data = parser.parse_args()
        title = data['title']
        description = data['description']
        todo_obj = Todo()
        todo_obj.title = title
        todo_obj.description = description
        todo_obj.user_id = description
        todo_obj.created_at = datetime.datetime.now()
        todo_obj.updated_at = datetime.datetime.now()
        db.session.add(todo_obj)
        db.session.commit()
        return jsonify({"message": "successfully created!"})

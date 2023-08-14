import datetime
from flask_restful import Resource, reqparse
from todo_app.data_access.sql_alchemy import db
from todo_app.data_access.models.models import Todo

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, required=True, help='Title is required')
parser.add_argument('description', type=str, required=False)


class TodoResource(Resource):

    def get(self, id):
        todo = Todo.query.get(id)
        if not todo:
            return {'message': 'Todo not found'}, 404
        return {'title': todo.title, 'description': todo.description}, 200

    def put(self, id):
        data = parser.parse_args()
        todo = Todo.query.get(id)
        if not todo:
            return {'message': 'Todo not found'}, 404
        todo.title = data['title']
        todo.description = data['description']
        db.session.commit()
        return {'message': 'Todo updated successfully'}, 200

    def delete(self, id):
        todo = Todo.query.get(id)
        if not todo:
            return {'message': 'Todo not found'}, 404
        db.session.delete(todo)
        db.session.commit()
        return {'message': 'Todo deleted successfully'}, 204


class TodoCreateResource(Resource):

    def get(self):
        todo = Todo.query.all()
        response = []
        for val in todo:
            response.append(
                {"title": val.title,
                 "description": val.description,
                 "created_at": str(val.created_at),
                 "updated_at": str(val.updated_at)
                 }
            )
        return response, 200

    def post(self):
        data = parser.parse_args()
        title = data['title']
        description = data['description']
        todo_obj = Todo()
        todo_obj.title = title
        todo_obj.description = description
        todo_obj.created_at = datetime.datetime.now()
        todo_obj.updated_at = datetime.datetime.now()
        db.session.add(todo_obj)
        db.session.commit()
        return ['created'], 201

from flask import jsonify, Blueprint, abort
from flask.ext.restful import (Resource, Api, reqparse,
                                marshal,marshal_with, fields, url_for)

import models

todo_fields = {
    'id':fields.Integer,
    'title':fields.String,
}

def todo_or_404(todo_id):
    try:
        todo = models.Todo.get(models.Todo.id==todo_id)
    except models.Todo.DoesNotExist:
        abort(404)
    else:
        return todo

class TodoList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'title',
            required = True,
            help = 'No todos title provided',
            location = ['form','json']


        )
        super().__init__()

    def get(self):
        todos = [marshal(todo,todo_fields) for todo in models.Todo.select()]
        return {'todos':todos}

    @marshal_with(todo_fields)
    def post(self):
        args = self.reqparse.parse_args()
        todo = models.Todo.create(**args)
        return (todo, 201,
                {'Location':url_for('resources.todos.todo',id=todo.id)}
                )




class Todo(Resource):
    @marshal_with(todo_fields)
    def get(self,id):
        return todo_or_404(id)

    @marshal_with(todo_fields)
    def put(self,id):
        args = self.reqparse.parse_args()
        try:
            todo = models.Todo.update(**args).where(models.Todo.id==id)
        except models.Todo.DoesNotExist:
            abort(404)
        else:
            return (todo, 201,
                    {'Location':url_for('resources.todos.todo',id=todo.id)}
                    )

    def delete(self,id):
        return jsonify({'name':'I need to get milk'})

todos_api = Blueprint('resources.todos',__name__)
api = Api(todos_api)
api.add_resource(
    TodoList,
    '/todos',
    endpoint='todos',
)
api.add_resource(
    Todo,
    '/todos/<int:id>',
    endpoint='todo',
)

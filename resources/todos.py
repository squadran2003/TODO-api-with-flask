from flask import Blueprint, abort, g
from flask.ext.restful import (Resource, Api, reqparse,
                               marshal, marshal_with, fields,
                               url_for)

import models

from auth import auth

todo_fields = {
    'id': fields.Integer,
    'name': fields.String,
}


def todo_or_404(todo_id):
    try:
        todo = models.Todo.get(models.Todo.id == todo_id)
    except models.Todo.DoesNotExist:
        abort(404)
    else:
        return todo


def get_users_todos():
    """this method gets all the todos belonging to the logged in user"""
    todos = models.Todo.select().where(models.Todo.user == g.user)
    return todos


class TodoList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No todos title provided',
            location=['form', 'json']


        )
        super().__init__()

    @auth.login_required
    @marshal_with(todo_fields)
    def get(self):
        print(g.user.id)
        todos = [marshal(todo, todo_fields) for todo in get_users_todos()]
        return (todos, 200, {'Location': url_for('resources.todos.todos')})

    @auth.login_required
    @marshal_with(todo_fields)
    def post(self):
        args = self.reqparse.parse_args()
        todo = models.Todo.create(user=g.user, **args)
        return (todo, 201,
                {'Location': url_for('resources.todos.todo', id=todo.id)}
                )


class Todo(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No todos title provided',
            location=['form', 'json']


        )
        super().__init__()

    @auth.login_required
    @marshal_with(todo_fields)
    def get(self, id):
        return todo_or_404(id)

    @auth.login_required
    @marshal_with(todo_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        try:
            query = models.Todo.update(**args).where(models.Todo.id == id)
            query.execute()
        except models.Todo.DoesNotExist:
            abort(404)
        else:
            return (todo_or_404(id), 201,
                    {'Location': url_for('resources.todos.todo', id=id)}
                    )

    @auth.login_required
    @marshal_with(todo_fields)
    def delete(self, id):
        try:
            query = models.Todo.delete().where(models.Todo.id == id)
            query.execute()
        except models.DoesNotExist:
            abort(404)
        else:
            return ('', 201, {'Location': url_for('resources.todos.todos')})


todos_api = Blueprint('resources.todos', __name__)
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

# TODO-api-with-flask
**Flask restful api for a todo app, this app is part of the 10th project as part of teamtreehouse techdegree.**

The frontend was built in angularjs


# Code Example

```
    from flask import Blueprint, abort, g
    from flask.ext.restful import (Resource, Api, reqparse,
                                    marshal,marshal_with, fields, url_for)

    import models

    from auth import auth

    todo_fields = {
        'id':fields.Integer,
        'name':fields.String,
    }

    def todo_or_404(todo_id):
        try:
            todo = models.Todo.get(models.Todo.id==todo_id)
        except models.Todo.DoesNotExist:
            abort(404)
        else:
            return todo


    def get_users_todos():
        """this method gets all the todos belonging to the logged in user"""
        todos = models.Todo.select().where(models.Todo.user==g.user)
        return todos


    class TodoList(Resource):
        def __init__(self):
            self.reqparse = reqparse.RequestParser()
            self.reqparse.add_argument(
                'name',
                required = True,
                help = 'No todos title provided',
                location = ['form','json']


            )
            super().__init__()


        @auth.login_required
        @marshal_with(todo_fields)
        def get(self):
            print(g.user.id)
            todos = [marshal(todo,todo_fields) for todo in get_users_todos()]
            return (todos,200,{'Location':url_for('resources.todos.todos')})

```

# Installation

clone the repo, create a virtualenv using python3
and run the commands below

```
   pip install -r requirements.txt
   python app.py

```

# Tests

To run the tests, follow the commands below

```
   coverage run tests.py
   coverage report --omit="lib/*"

```











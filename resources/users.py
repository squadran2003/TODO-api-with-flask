from flask import Blueprint, abort, make_response, json
from flask.ext.restful import (Resource, Api, reqparse,
                               marshal, marshal_with,
                               fields, url_for)

import models

user_fields = {
    'id': fields.Integer,
    'username': fields.String
}


def get_user_or_404(id):
    try:
        user = models.User.get(models.User.id == id)
    except models.User.DoesNotExist:
        abort(404)
    else:
        return user


class UserList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='No username provided',
            location=['form', 'json']

        )
        self.reqparse.add_argument(
            'email',
            required=True,
            help='No username provided',
            location=['form', 'json']

        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='No password provided',
            location=['form', 'json']

        )
        self.reqparse.add_argument(
            'verify_password',
            required=True,
            help='No verification of password provided',
            location=['form', 'json']

        )
        super().__init__()

    def get(self):
        users = [marshal(user, user_fields) for user in models.User.select()]
        return (users, 200, {'Location': url_for('resources.users.users')})

    @marshal_with(user_fields)
    def post(self):
        args = self.reqparse.parse_args()
        if args.get('password') == args.get('verify_password'):
            user = models.User.create_user(**args)
            return (user, 201)
        else:
            return make_response(json.dumps(
                                 {'error':
                                  'password and password verify do not match'
                                  }
                                 ), 400)


class User(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='No username provided',
            location=['form', 'json']

        )
        self.reqparse.add_argument(
            'email',
            required=True,
            help='No username provided',
            location=['form', 'json']

        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='No password provided',
            location=['form', 'json']

        )
        self.reqparse.add_argument(
            'verify_password',
            required=True,
            help='No verification of password provided',
            location=['form', 'json']

        )
        super().__init__()

    @marshal_with(user_fields)
    def get(self, username_or_email, password):
        try:
            user = models.User.get(
                (models.User.username == username_or_email) |
                (models.User.email == username_or_email)
            )
        except models.User.DoesNotExist:
            abort(404)
        else:
            if not user.verify_password(password):
                return (user, 400)
            else:
                return (user, 200)


users_api = Blueprint('resources.users', __name__)
api = Api(users_api)
api.add_resource(
    UserList,
    '/users',
    endpoint='users'
)
api.add_resource(
    User,
    '/users/<string:username_or_email>/<string:password>',
    endpoint='user'
)

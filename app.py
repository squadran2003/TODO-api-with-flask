from flask import Flask, g, jsonify, render_template, request
from auth import auth

import config
import models
from resources.todos import todos_api
from resources.users import users_api

app = Flask(__name__)
app.register_blueprint(users_api, url_prefix='/api/v1')
app.register_blueprint(todos_api, url_prefix='/api/v1')


@app.route('/')
def my_todos():
    if request.cookies.get('token'):
        return render_template('index.html')
    else:
        return render_template('login.html')


@app.route('/gettodos')
def gettodos():
    if not request.cookies.get('token'):
        return render_template('login.html')
    return render_template('index.html')


@app.route('/api/v1/users/token', methods=['GET'])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)

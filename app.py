from flask import Flask, g, jsonify,render_template
from auth import *

import config
import models
from resources.todos import todos_api
from resources.users import users_api

app = Flask(__name__)
app.register_blueprint(users_api,url_prefix='/api/v1')
app.register_blueprint(todos_api,url_prefix='/api/v1')


@app.route('/')
def my_todos():
    return render_template('index.html')


@app.route('/isAuthenticated')
def isAuthenticated():
    if basic_auth.username() or token_auth.username():
        return "1"
    else:
        return "2"


@app.route('/api/v1/users/token',methods=['GET'])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token':token.decode('ascii')})


if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)

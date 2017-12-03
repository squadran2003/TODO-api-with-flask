from flask import g
from flask.ext.httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
import models

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme="token")
auth = MultiAuth(token_auth,basic_auth)


@basic_auth.verify_password
def verify_password(username_or_email, password):
    try:
        user = models.User.get(
            (models.User.email==username_or_email)|
            (models.User.username==username_or_email)
        )
        if not user.verify_password(password):
            return False
    except models.User.DoesNotExist:
        return False
    else:
        g.user = user
        return True


@token_auth.verify_token
def verify_token(token):
    user = models.User.verify_auth_token(token)
    if user is not None:
        g.user = user
        return True
    else:
        return False

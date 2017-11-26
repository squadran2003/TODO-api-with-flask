import datetime

from argon2 import PasswordHasher
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)
from peewee import *

import config

DATABASE = SqliteDatabase('todos.sqlite')

class User(Model):
    username = CharField(unique=True)
    password = CharField()
    email = CharField(unique=True)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

class Todo(Model):
    name = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE



def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Todo], safe=True)
    DATABASE.close()

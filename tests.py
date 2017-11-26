import unittest,datetime
import requests
import json
import models
from flask.ext.restful import url_for


class TestTodoModel(unittest.TestCase):
    def setUp(self):
        self.todo = models.Todo.create(name="Get Milk from the shops")
        self.assertNotEqual(self.todo.created_at, datetime.datetime.now)

    def test_todo_list(self):
        todos = models.Todo.select()
        self.assertIn(self.todo,todos)



class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.user = models.User.create(username="abc",password="abc",
                                    email="abc@hotmail.com")
        self.assertNotEqual(self.user.created_at, datetime.datetime.now)

    def test_user_list(self):
        users = models.User.select()
        self.assertIn(self.user,users)


class TestTodoApi(unittest.TestCase):
    def setUp(self):
        self.todo = models.Todo.create(name="Get Milk from the shops")

    def test_todos_get(self):
        response = requests.get(url_for('resources.todos.todos'))
        self.assertContains(response.get_data(),self.todo.id)



if __name__=='__main__':
    unittest.main()

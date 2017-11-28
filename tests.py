import unittest,datetime, json
from app import app
import requests
from flask.ext.restful import url_for
import models



class TestTodoModel(unittest.TestCase):
    def setUp(self):
        self.todo = models.Todo.create(name="go swimming at 10")
        self.assertNotEqual(self.todo.created_at, datetime.datetime.now)

    def test_todo_list(self):
        todos = models.Todo.select()
        self.assertIn(self.todo,todos)



class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.user = models.User.create(username="andy4",password="andy4",
                                    email="andy4@hotmail.com")
        self.assertNotEqual(self.user.created_at, datetime.datetime.now)

    def test_user_list(self):
        users = models.User.select()
        self.assertIn(self.user,users)


class TestTodoApi(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.todo = models.Todo.create(name="Get Milk from the shops")

    def test_todos_get(self):
        response = self.client.get(url_for('resources.todos.todos'))
        myresponse = json.loads(response.get_data())
        self.assertTrue(self.check_id_in_json(myresponse,self.todo.id))

    def check_id_in_json(self,json_string, id):
        """this method takes a jsonstring and an id,
        loops over the json data and checks if the id is in
        its values"""

        for mydict in json_string:
            if id in mydict.values():
                return True




if __name__=='__main__':
    app.config['SERVER_NAME'] = '127.0.0.1:8000'
    with app.app_context():
        unittest.main()

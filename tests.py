import unittest,datetime, json
from app import app
import requests, base64
from flask.ext.restful import url_for
import models


class TestTodoModel(unittest.TestCase):
    def setUp(self):
        self.user = models.User.get(username="andy")
        self.todo = models.Todo.create(name="go swimming at 10",user=self.user)
        self.assertNotEqual(self.todo.created_at, datetime.datetime.now)

    def test_todo_list(self):
        todos = models.Todo.select().where(models.Todo.user==self.user)
        self.assertIn(self.todo,todos)


class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.user = models.User.get(username="andy")

    def test_user_list(self):
        users = models.User.select()
        self.assertIn(self.user,users)


class TestTodoApi(unittest.TestCase):
    def setUp(self):
        self.user = models.User.get(username="andy")
        self.client = app.test_client()
        self.headers = {
            'Authorization': 'Basic %s' % base64.b64encode(b"andy:123").decode("ascii")
        }
        self.todo = models.Todo.create(name="Get Milk from the shops",
                                            user = self.user)

    
    def test_todos_get(self):
        response = self.client.get(url_for('resources.todos.todos'),headers=self.headers)
        myresponse = json.loads(response.get_data())
        self.assertTrue(self.check_id_in_json(myresponse,self.todo.id))

    
    def test_todos_post(self):
        response = self.client.post(url_for('resources.todos.todos'),
                                    data={'name':'Go jogging at 10am',
                                                'user':self.user},headers=self.headers)
        myresponse = json.loads(response.get_data())
        self.assertEqual('Go jogging at 10am',myresponse.get('name'))

    def test_todos_put(self):
        response = self.client.put(url_for('resources.todos.todos'),
                                    data={'id':self.todo.id,
                                    'name':'Go jogging at 10am',
                                    'user':self.user},headers=self.headers)
        myresponse = json.loads(response.get_data())
        self.assertNotEqual(response.status_code,404)

    def test_todos_delete(self):
        response = self.client.delete(url_for('resources.todos.todos'),
                                    data={'id':self.todo.id,
                                    'name':'Go jogging at 10am'},headers=self.headers)
        myresponse = json.loads(response.get_data())
        self.assertNotEqual(response.status_code,404)


    def check_id_in_json(self,json_string, id):
        """this method takes a jsonstring and an id,
        loops over the json data and checks if the id is in
        its values"""

        for mydict in json_string:
            if id in mydict.values():
                return True

class TestUsersApi(unittest.TestCase):
    def setUp(self):
        self.user = models.User.get(username="andy")
        self.client = app.test_client()


    def test_users_get(self):
        response = self.client.get(url_for('resources.users.users'))
        myresponse = json.loads(response.get_data())
        self.assertTrue(self.check_username_in_json(myresponse))
    

    def check_username_in_json(self,json_string):
        """this method takes a jsonstring and an id,
        loops over the json data and checks if the id is in
        its values"""

        for mydict in json_string:
            if self.user.username in mydict.values():
                return True




if __name__=='__main__':
    app.config['SERVER_NAME'] = '127.0.0.1:8000'
    with app.app_context():
        unittest.main()

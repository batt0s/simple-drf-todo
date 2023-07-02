from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from todos.models import Todo
from rest_framework.authtoken.models import Token


class AccountTests(APITestCase):
    def test_register_user(self):
        """
        Ensure we can create a new user
        """
        url = reverse("register")
        data = {
            "username": "testing",
            "email": "testing@test.com",
            "password": "testt1234",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(data["username"], response.data["username"])
        self.assertEqual(1, User.objects.count())


class TodosTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testing", email="testing@test.com", password="testt1234")
        self.url_todos = reverse("apis:todos")
        self.test_todo = {
            "title": "TEST",
            "description": "test todo",
        }
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.headers = {
            'Authorization': 'Token '+ self.token.key,
        }

    def test_get_todos_un_authenticated(self):
        """
        Ensure we can't get any information without authentication
        """
        response = self.client.get(self.url_todos)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_create_todo_un_authenticated(self):
        """
        Ensure no one can create a todo without authentication
        """
        response = self.client.post(self.url_todos, self.test_todo, format="json")
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_create_todo_authenticated(self):
        """
        Ensure we can create a todo
        """
        response = self.client.post(self.url_todos, self.test_todo, headers=self.headers, format="json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.test_todo["title"], response.data["title"])
        self.assertEqual(self.test_todo["description"], response.data["description"])
        self.assertFalse(response.data["done"])
        self.assertEqual(self.user.id, response.data["owner"])
        self.assertEqual(1, Todo.objects.count())


class TodoTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testing", email="testing@test.com", password="testt1234")
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.headers = {
            'Authorization': 'Token ' + self.token.key,
        }
        self.url_todos = reverse("apis:todos")
        self.test_todo_object = Todo.objects.create(title="TEST", description="test todo", done=False, owner=self.user)
        self.url_todo = reverse("apis:todo", args=[self.test_todo_object.id])

    def test_get_todos(self):
        """
        Ensure we can get the list of the todos that we created
        """
        response = self.client.get(self.url_todos, headers=self.headers)
        data = response.data
        self.assertEqual(1, len(data))
        response_todo = data[0]
        self.assertEqual(self.test_todo_object.id, response_todo["id"])
        self.assertEqual(self.test_todo_object.title, response_todo["title"])
        self.assertEqual(self.user.id, response_todo["owner"])

    def test_view_todo_un_authenticated(self):
        """
        Ensure no one can view the todo without authentication
        """
        response = self.client.get(self.url_todo)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_view_todo(self):
        """
        Ensure we can get the details of a todo with its id
        """
        response = self.client.get(self.url_todo, headers=self.headers)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.test_todo_object.id, response.data["id"])
        self.assertEqual(self.test_todo_object.title, response.data["title"])

    def test_update_todo(self):
        """
        Ensure we can update the todo
        """
        update = {
            "description": "test todo updated",
            "done": True
        }
        response = self.client.put(self.url_todo, update, headers=self.headers)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.test_todo_object.id, response.data["id"])
        self.assertEqual(self.test_todo_object.title, response.data["title"])
        self.assertEqual(update["description"], response.data["description"])
        self.assertEqual(update["done"], response.data["done"])

    def test_delete_todo(self):
        """
        Ensure we can delete a todo
        """
        response = self.client.delete(self.url_todo, headers=self.headers)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

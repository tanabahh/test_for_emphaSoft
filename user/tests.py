from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
import json


class RightUserTest(APITestCase):
    def setUp(self):
        self.username = 'admin'
        self.password = 'admin'
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin')
        self.token = Token.objects.create(user=self.user)
        self.token.save()

    def test_token_auth(self):
        url = 'http://127.0.0.1:8000/api-token-auth/'
        data = {"username": self.username, "password": self.password}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.render().content)['token']
        self.assertEqual(json_response, self.token.key)

    def test_create_user(self):
        url = 'http://127.0.0.1:8000/api/users/'
        data = {'user': {'username': 'test_user', 'first_name': 'test',
                         'last_name': 'user', 'password': 'test_user',
                         'is_active': True}}
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION='Token {}'.format(self.token.key))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.render().content)
        self.assertEqual(json_response, "User 'test_user' created successfully")

    def test_get_users(self):
        url = 'http://127.0.0.1:8000/api/users/'
        response = self.client.get(url, HTTP_AUTHORIZATION='Token {}'.format(self.token.key))
        self.assertEqual(response.status_code, 200)
        correct_answer = {"users":
                              [{"username": "admin",
                                "first_name": "",
                                "last_name": "",
                                "is_active": True,
                                "last_login": None,
                                "is_superuser": True}]}
        json_response = json.loads(response.render().content)
        self.assertEqual(json_response, correct_answer)

    def test_get_user(self):
        url = 'http://127.0.0.1:8000/api/users/1'
        response = self.client.get(url, HTTP_AUTHORIZATION='Token {}'.format(self.token.key))
        self.assertEqual(response.status_code, 200)
        correct_answer = {"user": {
            "username": "admin",
            "first_name": "",
            "last_name": "",
            "is_active": True,
            "last_login": None,
            "is_superuser": True}}
        json_response = json.loads(response.render().content)
        self.assertEqual(json_response, correct_answer)

    def test_put_user(self):
        url = 'http://127.0.0.1:8000/api/users/1'
        data = {'user': {'username': 'new_user', 'first_name': 'test',
                         'last_name': 'user', 'password': 'new_user',
                         'is_active': True}}
        response = self.client.put(url, data, format='json', HTTP_AUTHORIZATION='Token {}'.format(self.token.key))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.render().content)
        self.assertEqual(json_response, "User 'new_user' updated successfully")

    def test_delete_user(self):
        user = User.objects.create_superuser('user_to_delete', 'user@user.com', 'user_to_delete')
        url = 'http://127.0.0.1:8000/api/users/2'
        response = self.client.delete(url, HTTP_AUTHORIZATION='Token {}'.format(self.token.key))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.render().content)
        self.assertEqual(json_response, "User 'user_to_delete' delete successfully")






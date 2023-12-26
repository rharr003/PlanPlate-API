from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
client = APIClient()

# Create your tests here.

class SignupViewTest(TestCase):
    def test_posting_with_valid_data(self):
        response = client.post(reverse("signup"), {"username": "test", "password": "test123"}, format="json")
        self.assertContains(response, "token")
        self.assertEqual(response.status_code, 200)
    
    def test_posting_with_incomplete_data(self):
        response = client.post(reverse("signup"), {"username": "test"}, format="json")
        self.assertEqual(response.status_code, 400)



class UserInfoView(TestCase):
    def setUp(self):
        User.objects.create_user(username="test", password="test123")

    def test_get_user_info_with_token(self):
        response = client.post(reverse("login"), {"username": "test", "password": "test123"}, format="json")
        self.assertContains(response, "token")
        token = response.data['token']
        self.assertIsInstance(token, str)
        header =  f"Token {token}"
        new_response = client.get(reverse("user"), format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(new_response.data['username'], "test")
        self.assertEqual(new_response.status_code, 200)
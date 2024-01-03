from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import CustomUser
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



class GetUserDetailViewTest(TestCase):
    def setUp(self):
        CustomUser.objects.create_user(username="test", password="test123")
        CustomUser.objects.create_user(username="admin", password="admin123", is_staff=True)

    def test_get_request_with_valid_auth(self):
        response = client.post(reverse("login"), {"username": "test", "password": "test123"}, format="json")
        self.assertContains(response, "token")
        token = response.data['token']
        self.assertIsInstance(token, str)
        header =  f"Token {token}"
        new_response = client.get(reverse("user"), format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(new_response.data['username'], "test")
        self.assertEqual(new_response.status_code, 200)
    
    def test_get_request_no_auth(self):
        response = client.get(reverse("user"), format="json")
        self.assertEqual(response.status_code, 401)
        
    
        
class DeleteUserDetailView(TestCase):
    def setUp(self):
        CustomUser.objects.create_user(username="test", password="test123")
        CustomUser.objects.create_user(username="admin", password="admin123", is_staff=True)
    def test_delete_request_with_admin_auth(self):
        response = client.post(reverse("login"), {"username": "admin", "password": "admin123"}, format="json")
        token = response.data['token']
        header =  f"Token {token}"
        user_to_delete = CustomUser.objects.get(username="test")
        self.assertEqual(len(CustomUser.objects.all()),2)
        delete_response = client.delete(reverse("user"), {"user_id": user_to_delete.id}, format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(delete_response.status_code, 204)
        self.assertEqual(delete_response.data, "Deleted test")
        self.assertEqual(len(CustomUser.objects.all()),1)
         
    def test_delete_request_with_no_auth(self):
        user_to_delete = CustomUser.objects.get(username="test")
        delete_response = client.delete(reverse("user"), {"user_id": user_to_delete.id}, format="json")
        self.assertEqual(delete_response.status_code, 401)
        
    def test_delete_request_with_admin_auth_with_invalid_user_id(self):
        response = client.post(reverse("login"), {"username": "admin", "password": "admin123"}, format="json")
        token = response.data['token']
        header =  f"Token {token}"
        delete_response = client.delete(reverse("user"), {"user_id": 9679769}, format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(delete_response.status_code, 404)
        
    def test_delete_request_with_admin_auth_with_no_user_id(self):
        response = client.post(reverse("login"), {"username": "admin", "password": "admin123"}, format="json")
        token = response.data['token']
        header =  f"Token {token}"
        delete_response = client.delete(reverse("user"), format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(delete_response.status_code, 400)
        
    def test_delete_request_with_correct_user_auth(self):
        response = client.post(reverse("login"), {"username": "test", "password": "test123"}, format="json")
        token = response.data['token']
        header =  f"Token {token}"
        user_to_delete = CustomUser.objects.get(username="test")
        self.assertEqual(len(CustomUser.objects.all()),2)
        delete_response = client.delete(reverse("user"), {"user_id": user_to_delete.id}, format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(delete_response.status_code, 204)
        self.assertEqual(delete_response.data, "Deleted test")
        self.assertEqual(len(CustomUser.objects.all()),1)
        
    def test_delete_request_with_wrong_user_auth(self):
        response = client.post(reverse("login"), {"username": "test", "password": "test123"}, format="json")
        token = response.data['token']
        header =  f"Token {token}"
        user_to_delete = CustomUser.objects.get(username="admin")
        delete_response = client.delete(reverse("user"), {"user_id": user_to_delete.id}, format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(delete_response.status_code, 401)
        self.assertEqual(len(CustomUser.objects.all()),2)
        
class PutUserDetailView(TestCase):
    def setUp(self):
        CustomUser.objects.create_user(username="test", password="test123")
        CustomUser.objects.create_user(username="admin", password="admin123", is_staff=True)
    def test_put_request_with_valid_fields(self):
        response = client.post(reverse("login"), {"username": "test", "password": "test123"}, format="json")
        token = response.data['token']
        header =  f"Token {token}"
        user_to_update = CustomUser.objects.get(username="test")
        put_response = client.put(reverse("user"), {"user_id": user_to_update.id, "username": "newTest"}, format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(put_response.status_code, 200 )
        updated_user = CustomUser.objects.get(pk=user_to_update.id)
        self.assertEqual(updated_user.username, "newTest")
        
    def test_put_request_with_invalid_fields(self):
        response = client.post(reverse("login"), {"username": "test", "password": "test123"}, format="json")
        token = response.data['token']
        header =  f"Token {token}"
        user_to_update = CustomUser.objects.get(username="test")
        put_response = client.put(reverse("user"), {"user_id": user_to_update.id, "happy_place": "bed"}, format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(put_response.status_code, 400 )
        
    def test_put_request_with_valid_and_invalid_fields(self):
        response = client.post(reverse("login"), {"username": "test", "password": "test123"}, format="json")
        token = response.data['token']
        header =  f"Token {token}"
        user_to_update = CustomUser.objects.get(username="test")
        put_response = client.put(reverse("user"), {"user_id": user_to_update.id, "username": "newTest", "favorite_color": "blue"}, format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(put_response.status_code, 200 )
        updated_user = CustomUser.objects.get(pk=user_to_update.id)
        self.assertEqual(updated_user.username, "newTest")

    
        
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from api.models import CustomUser
from fooditems.models import FoodItem
from .models import FoodServing
client = APIClient()

class GetUserFoodServingsTest(TestCase):
    def setUp(self):
        user1 = CustomUser.objects.create_user(username="test", password="test123")
        user2 = CustomUser.objects.create_user(username="admin", password="admin123", is_staff=True)
        CustomUser.objects.create_user(username="test2", password="test2123")
        f1 = FoodItem.objects.create(name="Ground Beef", base_serving_size=6,base_serving_size_unit="ounces", calories=280, fat=2, carbohydrates=0, protein=55, owner=user1)
        f1.save()
        f2 = FoodItem.objects.create(name="Chicken Breast", base_serving_size=3,base_serving_size_unit="ounces", calories=200, fat=2, carbohydrates=0, protein=55, owner=user1)
        f2.save()
        f3 = FoodItem.objects.create(name="Oatmeal", base_serving_size=3,base_serving_size_unit="ounces", calories=150, fat=2, carbohydrates=30, protein=6, owner=user2)
        f3.save()
        s1 = FoodServing.objects.create(serving_multiple=2, food_item=f1, owner=user1)
        s1.save()
        s2 = FoodServing.objects.create(serving_multiple=1, food_item=f2, owner=user1)
        s2.save()
        s3 = FoodServing.objects.create(serving_multiple=0.5, food_item=f3, owner=user2)
        s3.save()
        
    def test_get_request_returns_only_servings_owned_by_user(self):
        response = client.post(reverse("login"), {"username": "test", "password": "test123"}, format="json")
        token = response.data['token']
        header =  f"Token {token}"
        new_response = client.get(reverse("food_serving"), format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(len(new_response.data), 2)    
    
    def test_get_request_returns_empty_list_if_no_food_servings_by_owner(self):
        response = client.post(reverse("login"), {"username": "test2", "password": "test2123"}, format="json")
        token = response.data['token']
        header =  f"Token {token}"
        new_response = client.get(reverse("food_serving"), format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(len(new_response.data), 0)
    
class PostUserFoodServingsTest(TestCase):
    def setUp(self):
        user1 = CustomUser.objects.create_user(username="test", password="test123")
        user2 = CustomUser.objects.create_user(username="admin", password="admin123", is_staff=True)
        CustomUser.objects.create_user(username="test2", password="test2123")
        f1 = FoodItem.objects.create(name="Ground Beef", base_serving_size=6,base_serving_size_unit="ounces", calories=280, fat=2, carbohydrates=0, protein=55, owner=user1)
        f1.save()
        f2 = FoodItem.objects.create(name="Chicken Breast", base_serving_size=3,base_serving_size_unit="ounces", calories=200, fat=2, carbohydrates=0, protein=55, owner=user1)
        f2.save()
        f3 = FoodItem.objects.create(name="Oatmeal", base_serving_size=3,base_serving_size_unit="ounces", calories=150, fat=2, carbohydrates=30, protein=6, owner=user2)
        f3.save()
        s1 = FoodServing.objects.create(serving_multiple=2, food_item=f1, owner=user1)
        s1.save()
        s2 = FoodServing.objects.create(serving_multiple=1, food_item=f2, owner=user1)
        s2.save()
        s3 = FoodServing.objects.create(serving_multiple=0.5, food_item=f3, owner=user2)
        s3.save()
        
    def test_valid_post_request_adds_serving(self):
        response = client.post(reverse("login"), {"username": "test2", "password": "test2123"}, format="json")
        token = response.data['token']
        header =  f"Token {token}"
        food_item_id = FoodItem.objects.get(name="Ground Beef").id
        data = {
            "food_item_id": food_item_id,
            "serving_multiple": 1
        }
        second_response = client.get(reverse("food_serving"), format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(len(second_response.data), 0)
        third_response = client.post(reverse("food_serving"), data, format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(third_response.status_code, 200)
        final_response = client.get(reverse("food_serving"), format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(len(final_response.data), 1)  
    
    def test_invalid_post_request_returns_400(self): 
        response = client.post(reverse("login"), {"username": "test2", "password": "test2123"}, format="json")
        token = response.data['token']
        header =  f"Token {token}"
        data = {
            "hello": "world"
        }
        second_response = client.post(reverse("food_serving"), data, format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(second_response.status_code, 400)
        final_response = client.get(reverse("food_serving"), format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(len(final_response.data), 0)
        
class DeleteUserFoodServingsTest(TestCase): 
    def setUp(self):
        user1 = CustomUser.objects.create_user(username="test", password="test123")
        user2 = CustomUser.objects.create_user(username="admin", password="admin123", is_staff=True)
        CustomUser.objects.create_user(username="test2", password="test2123")
        f1 = FoodItem.objects.create(name="Ground Beef", base_serving_size=6,base_serving_size_unit="ounces", calories=280, fat=2, carbohydrates=0, protein=55, owner=user1)
        f1.save()
        f2 = FoodItem.objects.create(name="Chicken Breast", base_serving_size=3,base_serving_size_unit="ounces", calories=200, fat=2, carbohydrates=0, protein=55, owner=user1)
        f2.save()
        f3 = FoodItem.objects.create(name="Oatmeal", base_serving_size=3,base_serving_size_unit="ounces", calories=150, fat=2, carbohydrates=30, protein=6, owner=user2)
        f3.save()
        s1 = FoodServing.objects.create(serving_multiple=2, food_item=f1, owner=user1)
        s1.save()
        s2 = FoodServing.objects.create(serving_multiple=1, food_item=f2, owner=user1)
        s2.save()
        s3 = FoodServing.objects.create(serving_multiple=0.5, food_item=f3, owner=user2)
        s3.save()
        
    def test_valid_delete_request(self):
        response = client.post(reverse("login"), {"username": "test", "password": "test123"}, format="json")
        token = response.data['token']
        header =  f"Token {token}"
        serving = FoodServing.objects.get(serving_multiple=1)
        data = {
            "food_serving_id": serving.id
        }
        second_response = client.get(reverse("food_serving"), format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(len(second_response.data), 2)
        third_response = client.delete(reverse("food_serving"), data, format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(third_response.status_code, 204)
        final_response = client.get(reverse("food_serving"), format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(len(final_response.data), 1)
        
    def test_delete_request_with_wrong_user(self):
        response = client.post(reverse("login"), {"username": "test", "password": "test123"}, format="json")
        token = response.data['token']
        header =  f"Token {token}"
        serving = FoodServing.objects.get(serving_multiple=0.5)
        data = {
            "food_serving_id": serving.id
        }
        second_response = client.delete(reverse("food_serving"), data, format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(second_response.status_code, 401)
    
    def test_delete_request_with_bad_request(self):
        response = client.post(reverse("login"), {"username": "test", "password": "test123"}, format="json")
        token = response.data['token']
        header =  f"Token {token}"
        serving = FoodServing.objects.get(serving_multiple=0.5)
        data = {
            "food_seafasfasfgarving_id": serving.id
        }
        second_response = client.delete(reverse("food_serving"), data, format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(second_response.status_code, 400)
        
class PutUserFoodServingsTest(TestCase): 
    def setUp(self):
        user1 = CustomUser.objects.create_user(username="test", password="test123")
        user2 = CustomUser.objects.create_user(username="admin", password="admin123", is_staff=True)
        CustomUser.objects.create_user(username="test2", password="test2123")
        f1 = FoodItem.objects.create(name="Ground Beef", base_serving_size=6,base_serving_size_unit="ounces", calories=280, fat=2, carbohydrates=0, protein=55, owner=user1)
        f1.save()
        f2 = FoodItem.objects.create(name="Chicken Breast", base_serving_size=3,base_serving_size_unit="ounces", calories=200, fat=2, carbohydrates=0, protein=55, owner=user1)
        f2.save()
        f3 = FoodItem.objects.create(name="Oatmeal", base_serving_size=3,base_serving_size_unit="ounces", calories=150, fat=2, carbohydrates=30, protein=6, owner=user2)
        f3.save()
        s1 = FoodServing.objects.create(serving_multiple=2, food_item=f1, owner=user1)
        s1.save()
        s2 = FoodServing.objects.create(serving_multiple=1, food_item=f2, owner=user1)
        s2.save()
        s3 = FoodServing.objects.create(serving_multiple=0.5, food_item=f3, owner=user2)
        s3.save()
        
    def test_valid_request(self):
        response = client.post(reverse("login"), {"username": "test", "password": "test123"}, format="json")
        token = response.data['token']
        header =  f"Token {token}"
        serving = FoodServing.objects.get(serving_multiple=1)
        data = {
            "food_serving_id": serving.id,
            "serving_multiple": 5
        }
        second_response = client.put(reverse("food_serving"), data, format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(second_response.data['updated_item']['serving_multiple'], 5)
    
    def test_invalid_request(self):
        response = client.post(reverse("login"), {"username": "test", "password": "test123"}, format="json")
        token = response.data['token']
        header =  f"Token {token}"
        serving = FoodServing.objects.get(serving_multiple=1)
        data = {
            "food_serving_id": serving.id,
            "serviasdfasdf": "heloo"
        }
        second_response = client.put(reverse("food_serving"), data, format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(second_response.status_code, 400)
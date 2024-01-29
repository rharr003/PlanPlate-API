from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from api.models import CustomUser
from fooditems.models import FoodItem
from foodserving.models import FoodServing
from .models import Meal
client = APIClient() 


class GetUserMealsTest(TestCase):
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
        m1 = Meal.objects.create(name="breakfast", type="meal", owner=user1)
        m1.save()
        m2 = Meal.objects.create(name="lunch", type="meal", owner=user2)
        m2.save()
        m3 = Meal.objects.create(name="dinner", type="meal", owner=user2)
        m3.save()
        
    def test_get_request_returns_only_meals_owned_by_user(self):
        response = client.post(reverse("login"), {"username": "test", "password": "test123"}, format="json")
        token = response.data['token']
        header =  f"Token {token}"
        new_response = client.get(reverse("meal"), format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(len(new_response.data), 1)
        
    def test_get_request_returns_empty_list_if_user_has_no_meals(self):
        response = client.post(reverse("login"), {"username": "test2", "password": "test2123"}, format="json")
        token = response.data['token']
        header =  f"Token {token}"
        new_response = client.get(reverse("meal"), format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(len(new_response.data), 0)
        
class PostUserMealsTest(TestCase):
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
        m1 = Meal.objects.create(name="breakfast", type="meal", owner=user1)
        m1.save()
        m2 = Meal.objects.create(name="lunch", type="meal", owner=user2)
        m2.save()
        m3 = Meal.objects.create(name="dinner", type="meal", owner=user2)
        m3.save()
        
    def test_valid_post_request_works(self):
        auth_response = client.post(reverse("login"), {"username": "test2", "password": "test2123"}, format="json")
        token = auth_response.data['token']
        header =  f"Token {token}"
        data = {
            "name": "brunch",
            "type": "snack"
        }
        post_response = client.post(reverse("meal"), data, format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(post_response.status_code, 200)
        get_response = client.get(reverse("meal"), format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(len(get_response.data), 1)
    
    def test_invalid_post_request_does_nothing(self):
        auth_response = client.post(reverse("login"), {"username": "test2", "password": "test2123"}, format="json")
        token = auth_response.data['token']
        header =  f"Token {token}"
        data = {
            "name": "brunch",
            "typeadfadf": "snack"
        }
        post_response = client.post(reverse("meal"), data, format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(post_response.status_code, 400)
        get_response = client.get(reverse("meal"), format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(len(get_response.data), 0)
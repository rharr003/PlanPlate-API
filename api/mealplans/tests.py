from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from api.models import CustomUser
from fooditems.models import FoodItem
from foodserving.models import FoodServing
from meals.models import Meal
from .models import MealPlan
client = APIClient()

class GetUserMealPlansTest(TestCase):
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
        mp1 = MealPlan.objects.create(name="Diet 1", active=True, owner=user1)
        mp1.save()
        mp2 = MealPlan.objects.create(name="Diet 2", active=False, owner=user2)
        mp2.save()
        mp3 = MealPlan.objects.create(name="Diet 3", active=False, owner=user2)
        mp3.save()
        
        
    def test_get_request_returns_only_meal_plans_owned_by_user(self):
        response = client.post(reverse("login"), {"username": "test", "password": "test123"}, format="json")
        token = response.data['token']
        header =  f"Token {token}"
        new_response = client.get(reverse("meal_plan"), format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(len(new_response.data['inactive']), 0)
        self.assertEqual(new_response.data['active']['name'], "Diet 1")
        
    def test_get_request_returns_empty_list_if_user_has_no_meal_plans(self):
        response = client.post(reverse("login"), {"username": "test2", "password": "test2123"}, format="json")
        token = response.data['token']
        header =  f"Token {token}"
        new_response = client.get(reverse("meal_plan"), format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(len(new_response.data['inactive']), 0)
        self.assertEqual(len(new_response.data['active']), 0)
        
class PostUserMealPlansTest(TestCase):
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
        mp1 = MealPlan.objects.create(name="Diet 1", active=True, owner=user1)
        mp1.save()
        mp2 = MealPlan.objects.create(name="Diet 2", active=False, owner=user2)
        mp2.save()
        mp3 = MealPlan.objects.create(name="Diet 3", active=False, owner=user2)
        mp3.save()
        
        
    def test_valid_post_request_adds_meal_plan(self):
        auth_response = client.post(reverse("login"), {"username": "test", "password": "test123"}, format="json")
        token = auth_response.data['token']
        header =  f"Token {token}"
        initial_get_response = client.get(reverse("meal_plan"), format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(len(initial_get_response.data['inactive']), 0)
        self.assertEqual(initial_get_response.data['active']['name'], "Diet 1")
        data = {
            "name": "New Meal",
            "active": False
        }
        post_response = client.post(reverse("meal_plan"), data, format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(post_response.status_code, 200)
        final_get_response = client.get(reverse("meal_plan"), format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(len(final_get_response.data['inactive']), 1)
        self.assertEqual(final_get_response.data['active']['name'], "Diet 1")
        
    def test_invalid_post_request_does_nothing(self):
        auth_response = client.post(reverse("login"), {"username": "test", "password": "test123"}, format="json")
        token = auth_response.data['token']
        header =  f"Token {token}"
        initial_get_response = client.get(reverse("meal_plan"), format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(len(initial_get_response.data['inactive']), 0)
        self.assertEqual(initial_get_response.data['active']['name'], "Diet 1")
        data = {
            "nameasdfasdf": "New Meal",
            "active": False
        }
        post_response = client.post(reverse("meal_plan"), data, format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(post_response.status_code, 400)
        final_get_response = client.get(reverse("meal_plan"), format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(len(final_get_response.data['inactive']),0)
        self.assertEqual(final_get_response.data['active']['name'], "Diet 1")
        
class DeleteUserMealPlansTest(TestCase):
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
        mp1 = MealPlan.objects.create(name="Diet 1", active=True, owner=user1)
        mp1.save()
        mp2 = MealPlan.objects.create(name="Diet 2", active=False, owner=user2)
        mp2.save()
        mp3 = MealPlan.objects.create(name="Diet 3", active=False, owner=user2)
        mp3.save()
        
    def test_valid_delete_request_deletes_meal_plan(self):
        auth_response = client.post(reverse("login"), {"username": "test", "password": "test123"}, format="json")
        token = auth_response.data['token']
        header =  f"Token {token}"
        initial_get_response = client.get(reverse("meal_plan"), format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(len(initial_get_response.data['inactive']), 0)
        self.assertEqual(initial_get_response.data['active']['name'], "Diet 1")
        meal_plan_to_delete_id = MealPlan.objects.get(name="Diet 1").id
        data =  {
            "meal_plan_id": meal_plan_to_delete_id
        }
        delete_response = client.delete(reverse("meal_plan"), data, format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(delete_response.status_code, 200)
        final_get_response = client.get(reverse("meal_plan"), format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(len(final_get_response.data['inactive']),0)
        self.assertEqual(final_get_response.data['active'], [])
        
        
    def test_invalid_delete_request_does_nothing(self):
        auth_response = client.post(reverse("login"), {"username": "test", "password": "test123"}, format="json")
        token = auth_response.data['token']
        header =  f"Token {token}"
        initial_get_response = client.get(reverse("meal_plan"), format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(len(initial_get_response.data['inactive']), 0)
        self.assertEqual(initial_get_response.data['active']['name'], "Diet 1")
        meal_plan_to_delete_id = MealPlan.objects.get(name="Diet 1").id
        data =  {
            "meal_plan_adfasdfid": meal_plan_to_delete_id
        }
        delete_response = client.delete(reverse("meal_plan"), data, format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(delete_response.status_code, 400)
        final_get_response = client.get(reverse("meal_plan"), format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(len(final_get_response.data['inactive']),0)
        self.assertEqual(final_get_response.data['active']['name'], "Diet 1")
    
    def test_unauth_delete_request_does_nothing(self):
        auth_response = client.post(reverse("login"), {"username": "test2", "password": "test2123"}, format="json")
        token = auth_response.data['token']
        header =  f"Token {token}"
        meal_plan_to_delete_id = MealPlan.objects.get(name="Diet 1").id
        data =  {
            "meal_plan_id": meal_plan_to_delete_id
        }
        delete_response = client.delete(reverse("meal_plan"), data, format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(delete_response.status_code, 401)
        second_auth_response = client.post(reverse("login"), {"username": "test", "password": "test123"}, format="json")
        second_token = second_auth_response.data['token']
        second_header =  f"Token {second_token}"
        final_get_response = client.get(reverse("meal_plan"), format="json", HTTP_AUTHORIZATION=second_header)
        self.assertEqual(len(final_get_response.data['inactive']),0)
        self.assertEqual(final_get_response.data['active']['name'], "Diet 1")
        
class PutUserMealPlansTest(TestCase):
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
        mp1 = MealPlan.objects.create(name="Diet 1", active=True, owner=user1)
        mp1.save()
        mp2 = MealPlan.objects.create(name="Diet 2", active=False, owner=user2)
        mp2.save()
        mp3 = MealPlan.objects.create(name="Diet 3", active=False, owner=user2)
        mp3.save()
        
    def test_valid_put_request_works(self):
        auth_response = client.post(reverse("login"), {"username": "test", "password": "test123"}, format="json")
        token = auth_response.data['token']
        header =  f"Token {token}"
        initial_get_response = client.get(reverse("meal_plan"), format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(len(initial_get_response.data['inactive']), 0)
        self.assertEqual(initial_get_response.data['active']['name'], "Diet 1")
        meal_plan_to_delete_id = MealPlan.objects.get(name="Diet 1").id
        data =  {
            "meal_plan_id": meal_plan_to_delete_id,
            "name": "New Name"
        }
        put_response = client.put(reverse("meal_plan"), data, format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(put_response.status_code, 200)
        final_get_response = client.get(reverse("meal_plan"), format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(len(final_get_response.data['inactive']),0)
        self.assertEqual(final_get_response.data['active']['name'], "New Name")
        
    def test_invalid_put_request_does_nothing(self):
        auth_response = client.post(reverse("login"), {"username": "test", "password": "test123"}, format="json")
        token = auth_response.data['token']
        header =  f"Token {token}"
        initial_get_response = client.get(reverse("meal_plan"), format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(len(initial_get_response.data['inactive']), 0)
        self.assertEqual(initial_get_response.data['active']['name'], "Diet 1")
        meal_plan_to_delete_id = MealPlan.objects.get(name="Diet 1").id
        data =  {
            "meal_plan_id": meal_plan_to_delete_id,
            "nameasdfasdf": "New Name",
            "elmo": True
        }
        put_response = client.put(reverse("meal_plan"), data, format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(put_response.status_code, 200)
        final_get_response = client.get(reverse("meal_plan"), format="json", HTTP_AUTHORIZATION=header)
        self.assertEqual(len(final_get_response.data['inactive']),0)
        self.assertEqual(final_get_response.data['active']['name'], "Diet 1")
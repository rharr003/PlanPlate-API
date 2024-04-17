# Meal Planning API Overview

## Basics

The Meal Planning API is a REST API that allows for the storing and organizing of various meal plans. At its core you can use it to store information about ingredients, portion sizes, meals, and meal plans.

## Authentication

To get started you will need to get to create an account by submitting a POST request to
[signup_url](/auth/signup) or to [login_url](/auth/login) providing the following required keys in the request body:

```
    {
        "username": [varchar150],
        "password": [varchar]
    }
```

Upon sending a valid request to either of the above end points, you will recieve a response with a token that will look like this:

```
    {
        "token": <authtoken>
    }
```

This token will need to be added to all subsequent request headers:

```
    {
        ...headers,
        Authorization: "Token <authtoken>"
    }
```

With this header included you should have full access to all the routes. Currently the auth tokens have no expiry.

## Food Items

Food Items are the base ingredient that will be used to comprise various Food Servings which can then be added to Meals.

### Food Item Routes:

#### Main:

Base url: [food_items_base_url](/fooditems)

##### GET:

Returns an unordered list of all food items owned by current user

##### POST:

Adds a new food item. Request body should look like this:

```
    {
        "name": [String],
        "base_serving_size": [Float],
        "base_serving_unit": [String(gram, ounce, cup, etc...)]
        "calories": [Integer],
        "fat": [Float],
        "saturated_fat": [Float(optional)],
        "carbohydrates": [Float],
        "fiber": [Float(optional)],
        "sugar": [Float(optional)],
        "protein": [Float],
        "sodium": [Integer(optional)],
        "potassium": [Integer(optional)]
   }
```

The owner of a food item is automatically assigned based on the authorization headers

Returns the created food item

##### DELETE:

Deletes the specified food item. Request body should look like this:

```
    {
        "food_item_id": [Integer]
    }
```

Returns confirmation message upon successful deletion

##### PUT:

Updates the specified food item. Request body should look like this:

All fields are optional. Must included atleast 1 proper field. Incorrect fields will be ignored

```
    {
        "name": [String],
        "base_serving_size": [Float],
        "base_serving_unit": [String(gram, ounce, cup, etc...)]
        "calories": [Integer],
        "fat": [Float],
        "saturated_fat": [Float(optional)],
        "carbohydrates": [Float],
        "fiber": [Float(optional)],
        "sugar": [Float(optional)],
        "protein": [Float],
        "sodium": [Integer(optional)],
        "potassium": [Integer(optional)]
   }
```

Returns the updated food item

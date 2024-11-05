from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

from shop.models import Product

class Test(APITestCase):
    user = None

    def get_or_create_test_user(self):
        if not self.user:
            self.user = User.objects.create_user('testuser', 'test@example.com', 'password123')
            return self.user
        else:
            return self.user

    def post(self, url, data=None, expected_status_code=status.HTTP_201_CREATED):
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, expected_status_code)
        return response

    def put(self, url, data=None, expected_status_code=status.HTTP_200_OK):
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, expected_status_code)
        return response

    def patch(self, url, data=None, expected_status_code=status.HTTP_200_OK):
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, expected_status_code)
        return response

    def delete(self, url, expected_status_code=status.HTTP_200_OK):
        response = self.client.delete(url)
        self.assertEqual(response.status_code, expected_status_code)
        return response

    def get(self, url, expected_status_code=status.HTTP_200_OK):
        response = self.client.get(url)
        self.assertEqual(response.status_code, expected_status_code)
        return response

    def authenticate(self):
        user = self.get_or_create_test_user()
        self.api_token = Token.objects.get_or_create(user=user)[0]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.api_token.key)


    def test_api_products_list(self):
        self.authenticate()
        res = self.get(reverse('api:products'), expected_status_code=status.HTTP_200_OK)

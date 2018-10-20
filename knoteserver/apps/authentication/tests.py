from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class AccountTests(APITestCase):
    def test_create_account(self):
        url = reverse('auth:register')
        data = {
            'username': 'testuser',
            'email': 'hello@test.net',
            'password': 'Testpwd@1'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(get_user_model().objects.count(), 1, response.data)
        self.assertEqual(get_user_model().objects.get(username='testuser').username, 'testuser', response.data)

    def test_create_account_without_email(self):
        url = reverse('auth:register')
        data = {
            'username': 'testuser',
            'password': 'Testpwd@1'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)

    def test_login(self):
        reg_url = reverse('auth:register')
        data = {
            'username': 'testuser',
            'email': 'hello@test.net',
            'password': 'Testpwd@1'
        }
        response = self.client.post(reg_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

        url = reverse('auth:login')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertTrue(response.data['token'])

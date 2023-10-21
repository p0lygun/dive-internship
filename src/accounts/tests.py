from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class TestCaseBase(APITestCase):
    @property
    def bearer_token(self):
        # assuming there is a user in User model
        user = User.objects.create_user(
            username='test_user', password='12345678'
        )

        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION": f'Bearer {refresh.access_token}'}


class LoginTestClass(TestCaseBase):
    url = reverse('check_login')

    def test_no_auth(self):
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.data
        )

    def test_auth(self):
        response = self.client.get(self.url, **self.bearer_token)
        valid_response_data = {
            "login": True,
            "user": {
                "id": 1,
                "username": "test_user"
            }
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, valid_response_data)

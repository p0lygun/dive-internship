from django.urls import reverse
from rest_framework import status

from ..helper.tests import TestCaseBase


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

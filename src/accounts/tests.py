from django.urls import reverse
from rest_framework import status

from helper.tests import TestCaseBase, set_up_data


class LoginTestClass(TestCaseBase):
    users = dict()

    @classmethod
    def setUpTestData(cls):
        set_up_data(cls)

    url = reverse('check_login')

    def test_no_auth(self):
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.data
        )

    def test_auth(self):
        response = self.client.get(self.url, headers=self.bearer_token)
        valid_response_data = {
            "login": True,
            "user": {
                "id": 1,
                "username": "test_normal_user",
                "calories_per_day": 0
            }
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, valid_response_data)

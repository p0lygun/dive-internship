import os

from django.urls import reverse
from rest_framework import status

from helper.tests import TestCaseBase


class EntryCreationTest(TestCaseBase):
    url = reverse('entries')
    entry = {
        "description": "Milk",
        "calories": 122
    }

    def test_normal_user_create_entry(self):
        # print(os.environ)
        response = self.client.post(
            self.url,
            data=self.entry,
            headers=self.bearer_token
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_manager_create_entry(self):

        response = self.client.post(
            self.url,
            data=self.entry,
            headers=self.manager_bearer_token
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_create_entry(self):

        response = self.client.post(
            self.url,
            data=self.entry,
            headers=self.admin_bearer_token
        )

        assert response.status_code == status.HTTP_201_CREATED

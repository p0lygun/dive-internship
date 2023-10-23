import os

from django.urls import reverse
from rest_framework import status

from helper.tests import TestCaseBase, set_up_data


class EntryCreationTest(TestCaseBase):
    users = dict()

    url = reverse('entries')
    entry = {
        "description": "Milk",
        "calories": 122
    }

    @classmethod
    def setUpTestData(cls):
        set_up_data(cls)

    def test_normal_user_create_entry(self):
        # print(os.environ)
        response = self.client.post(
            self.url,
            data=self.entry,
            headers=self.bearer_token
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_manager_create_entry(self):

        response = self.client.post(
            self.url,
            data=self.entry,
            headers=self.manager_bearer_token
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_create_entry(self):

        response = self.client.post(
            self.url,
            data=self.entry,
            headers=self.admin_bearer_token
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CaloriesLogicTest(TestCaseBase):
    users = dict()

    @classmethod
    def setUpTestData(cls):
        set_up_data(cls)

    def test_setting_calories_per_day(self):
        normal_user_id = self.users['normal'].id
        url = reverse('api-users-detail', args=str(normal_user_id,))
        new_calories_per_day = 100
        response = self.client.patch(
            url,
            headers=self.manager_bearer_token,
            data={
                "calories_per_day": new_calories_per_day
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['entry']['calories_per_day'], new_calories_per_day)

    def test_calories_per_day(self):
        calories_per_day = self.users['normal'].calories_per_day

        url = reverse('entries')
        # add entry
        entry = {
            "description": "Milk",
            "calories": 122
        }
        is_under_total_calories = calories_per_day > entry['calories']
        response = self.client.post(
            url,
            headers=self.bearer_token,
            data=entry
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        entry_id = response.data['data']['entry']['id']

        # get entry
        url = reverse('entry-detail', args=(str(entry_id),))
        response = self.client.get(
            url,
            headers=self.bearer_token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['entry']['is_under_total_calories'], is_under_total_calories)




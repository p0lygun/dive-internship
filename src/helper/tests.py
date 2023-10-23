import os
from django.contrib.auth import get_user_model, models
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def set_up_data(cls):
    if len(cls.users.keys()) == 0:
        for index, group_name in enumerate(["normal", "manager", "admin"], start=1):
            user, created = User.objects.get_or_create(
                username=f'test_{group_name}_user', password='12345678'
            )
            group, created = models.Group.objects.get_or_create(name=group_name)
            group.user_set.add(user)
            cls.users[group_name] = user


class TestCaseBase(APITestCase):
    users = dict()

    @property
    def bearer_token(self):
        refresh = RefreshToken.for_user(self.users['normal'])
        return {
            "Authorization": f'Bearer {refresh.access_token}'
        }

    @property
    def manager_bearer_token(self):
        refresh = RefreshToken.for_user(self.users['manager'])
        return {
            "Authorization": f'Bearer {refresh.access_token}'
        }

    @property
    def admin_bearer_token(self):
        refresh = RefreshToken.for_user(self.users['admin'])
        return {
            "Authorization": f'Bearer {refresh.access_token}'
        }



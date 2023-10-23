import os
from django.contrib.auth import get_user_model, models
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class TestCaseBase(APITestCase):

    @property
    def bearer_token(self):
        user = User.objects.create_user(
            username='test_user', password='12345678'
        )
        normal_group, created = models.Group.objects.get_or_create(name="normal")
        normal_group.user_set.add(user)

        refresh = RefreshToken.for_user(user)
        return {"Authorization": f'Bearer {refresh.access_token}'}

    @property
    def manager_bearer_token(self):
        user = User.objects.create_user(
            username='test_manager_user', password='12345678'
        )
        group, created = models.Group.objects.get_or_create(name="manager")
        group.user_set.add(user)

        refresh = RefreshToken.for_user(user)
        return {"Authorization": f'Bearer {refresh.access_token}'}

    @property
    def admin_bearer_token(self):
        user = User.objects.create_user(
            username='test_admin_user', password='12345678'
        )
        group, created = models.Group.objects.get_or_create(name="admin")
        group.user_set.add(user)

        refresh = RefreshToken.for_user(user)
        return {"Authorization": f'Bearer {refresh.access_token}'}



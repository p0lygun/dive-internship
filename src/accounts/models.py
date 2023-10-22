from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    calories_per_day = models.PositiveIntegerField(default=0, null=False, blank=False)

    def __str__(self):
        return self.username

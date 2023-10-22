from django.db import models
from django.conf import settings


class Entry(models.Model):
    time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    description = models.TextField(blank=False)
    calories = models.PositiveIntegerField(help_text="Total Number of calories in an entry", null=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.description[0:20]

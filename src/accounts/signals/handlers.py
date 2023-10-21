from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=get_user_model())
def add_user_to_group(sender, instance, created, **kwargs):
    user = instance
    if created:
        group = Group.objects.get(name='normal')
        user.groups.add(group)

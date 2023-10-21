import os

from django.apps import AppConfig
from loguru import logger


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        if os.environ.get('RUN_MAIN'):
            logger.info("Setting up accounts app config....")

            from django.contrib.auth.models import Group
            from django.contrib.auth.models import Permission

            GROUPS = {
                "normal": ['entry'],
                "manager": ['customuser'],
                "admin": ['entry', 'customuser']
            }
            PERMISSIONS = ['add', "change", "view", "delete"]
            for group, models in GROUPS.items():
                group: Group
                group, created = Group.objects.get_or_create(name=group)
                if created:
                    logger.info(f'{group} Created')
                    group_permissions = []
                    for model in models:
                        for permission_name in PERMISSIONS:
                            codename = f"{permission_name}_{model}"
                            permission = Permission.objects.get(codename=codename)
                            group_permissions.append(permission)
                    group.permissions.set(group_permissions)
                else:
                    # todo: add all perms if not on group.
                    logger.info(f'{group} Exists')

            # register signals
            from .signals import handlers  # just importing is fine


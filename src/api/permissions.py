from django.contrib.auth.models import Group
from rest_framework import permissions


def is_in_group(user, group_name):
    """
    Takes a user and a group name, and returns `True` if the user is in that group.
    """
    try:
        return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()
    except Group.DoesNotExist:
        return None


class HasGroupPermission(permissions.BasePermission):
    """
    Ensure user is in required groups.
    """

    def has_permission(self, request, view):
        # Get a mapping of methods -> required group.
        allowed_groups = getattr(view, "allowed_groups", [])

        # return true is use in group or is staff
        return any(
            [
                is_in_group(request.user, group_name)
                if group_name != "__all__" else True
                for group_name in allowed_groups
            ]) or (request.user and request.user.is_staff)

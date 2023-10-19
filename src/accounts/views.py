from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets, permissions

from . import serializers as account_serializers


class SignUpUserView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = get_user_model().objects.all()
    serializer_class = account_serializers.SignupSerializer

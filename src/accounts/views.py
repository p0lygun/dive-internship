from django.contrib.auth import get_user_model

from rest_framework import mixins, viewsets, permissions, status
from rest_framework.views import APIView, Response

from . import serializers as account_serializers


class SignUpUserView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = get_user_model().objects.all()
    serializer_class = account_serializers.SignupSerializer


class CheckLoginView(APIView):
    def get(self, request):
        user = request.user
        serialized_user = account_serializers.UserSerializer(user)
        return Response(
            {
                'login': True,
                'user': serialized_user.data
            },
            status.HTTP_200_OK
        )


import django.core.exceptions
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from rest_framework.views import Response, status
from rest_framework.views import APIView

from rest_framework.generics import GenericAPIView, ListAPIView

from .. import permissions
from accounts import serializers, models


class UserBaseView(APIView):
    model = get_user_model()
    permission_classes = [permissions.HasGroupPermission]
    allowed_groups = ['manager', 'admin']
    queryset = Group.objects.get(name="normal").user_set.all()
    serializer_class = serializers.UserSerializer


class UserView(UserBaseView, ListAPIView):

    def post(self, request):
        serializer = serializers.SignupSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            return Response(
                {
                    "status": "success",
                    "data": {
                        "user": self.get_serializer(new_user).data
                    }
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                    "status": "fail",
                    "message": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class UserDetailView(UserBaseView, GenericAPIView):

    def get_user(self, pk) -> models.CustomUser | None:
        try:
            return self.queryset.get(pk=pk)
        except django.core.exceptions.ObjectDoesNotExist:
            return None

    def get(self, request, pk):
        user = self.get_user(pk)
        if user is None:
            return Response(
                {
                    "status": "fail",
                    "message": f"User not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {
                "status": "success",
                "entry": self.get_serializer(user).data,
            },
            status=status.HTTP_200_OK
        )

    def patch(self, request, pk):
        user = self.get_user(pk)
        if user is None:
            return Response(
                {
                    "status": "fail",
                    "message": f"User with Id: {pk} not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = serializers.SignupSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": {"note": serializer.data}})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_user(pk)
        if user is None:
            return Response(
                {
                    "status": "fail", "message": f"User with Id: {pk} not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

import django.core.exceptions
from rest_framework.views import Response, status
from rest_framework.generics import GenericAPIView, ListAPIView

from . import models, serializers, permissions


class EntryItemBaseView:
    model = models.Entry
    permission_classes = [permissions.HasGroupPermission]
    allowed_groups = ['normal', 'admin']
    serializer = serializers.EntrySerializer
    queryset = models.Entry.objects.all()


class EntryItemView(EntryItemBaseView, ListAPIView):

    def get_serializer_class(self):
        if permissions.is_in_group(self.request.user, "admin"):
            return self.serializer

        return serializers.EntrySerializerForUser

    def get_queryset(self):
        user = self.request.user
        entries = self.queryset

        if permissions.is_in_group(user, "normal"):
            entries = self.queryset.filter(owner=user)

        return entries

    def post(self, request):
        data = request.data
        data['owner'] = request.user.id
        serializer = self.serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "success",
                    "data": {
                        "entry": data
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


class EntryItemDetailView(EntryItemBaseView):
    def get_entry(self, pk) -> models.Entry | None:
        try:
            return self.model.objects.get(pk=pk)
        except django.core.exceptions.ObjectDoesNotExist:
            return None

    def get(self, request, pk):
        entry = self.get_entry(pk)
        if entry is None:
            return Response(
                {
                    "status": "fail",
                    "message": f"entry object not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if permissions.is_in_group(request.user, "admin"):
            return Response(
                {
                    "status": "success",
                    "entry": self.serializer(entry).data,
                },
                status=status.HTTP_200_OK
            )

        if entry.owner != request.user:
            return Response(
                {
                    "status": "fail",
                    "message": "Not allowed to access other owner entries"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(
            {
                "status": "success",
                "entry": serializers.EntrySerializerForUser(entry).data
            },
            status=status.HTTP_200_OK
        )

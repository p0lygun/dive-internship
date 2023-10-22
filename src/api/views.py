import django.core.exceptions
from rest_framework.views import Response, status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView

from . import models, serializers, permissions


class EntryItemBaseView(APIView):
    model = models.Entry
    permission_classes = [permissions.HasGroupPermission]
    allowed_groups = ['normal', 'admin']
    queryset = models.Entry.objects.all()

    def get_serializer_class(self):
        if permissions.is_in_group(self.request.user, "admin"):
            return serializers.EntrySerializer

        return serializers.EntrySerializerForUser


class EntryItemView(EntryItemBaseView, ListAPIView):

    def get_queryset(self):
        user = self.request.user
        entries = self.queryset

        if permissions.is_in_group(user, "normal"):
            entries = self.queryset.filter(owner=user)

        return entries

    def post(self, request):
        data = request.data
        data['owner'] = request.user.id
        serializer = self.get_serializer(data=data)
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


class EntryItemDetailView(EntryItemBaseView, GenericAPIView):
    permission_classes = [*EntryItemBaseView.permission_classes, permissions.IsOwnerOrAdmin]

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
        return Response(
            {
                "status": "success",
                "entry": self.get_serializer(entry).data,
            },
            status=status.HTTP_200_OK
        )

    def patch(self, request, pk):
        entry = self.get_entry(pk)
        if entry is None:
            return Response(
                {
                    "status": "fail",
                    "message": f"Note with Id: {pk} not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        request.data.pop('owner', None)
        request.data.pop('time', None)

        serializer = self.get_serializer(entry, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": {"note": serializer.data}})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        entry = self.get_entry(pk)
        if entry is None:
            return Response(
                {
                    "status": "fail", "message": f"Note with Id: {pk} not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

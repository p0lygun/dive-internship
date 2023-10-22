from rest_framework.views import Response, status
from rest_framework.generics import GenericAPIView

from . import models, serializers, permissions


class EntryItemView(GenericAPIView):
    permission_classes = [permissions.HasGroupPermission]
    allowed_groups = ['normal', 'admin']

    serializer = serializers.EntrySerializer
    queryset = models.Entry.objects.all()

    def get(self, request):
        if permissions.is_in_group(request.user, "admin"):
            entries_serialized = serializers.EntrySerializer(self.queryset, many=True)
        else:
            entries_serialized = serializers.EntrySerializerForUser(
                self.queryset.filter(owner=request.user), many=True
            )

        response_data = {
            'entries': entries_serialized.data
        }

        return Response(
            response_data,
            status=status.HTTP_200_OK
        )

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





from rest_framework.views import APIView, Response, status

from . import models, serializers


class EntryItemView(APIView):

    def get(self, request):
        qs = models.Entry.objects.all()

        # todo: check for admin permission and 404 for "manager" kind user
        if request.user.is_superuser:
            entries_serialized = serializers.EntrySerializer(qs, many=True)
        else:
            entries_serialized = serializers.EntrySerializerForUser(
                qs.filter(owner=request.user), many=True
            )

        response_data = {
            'entries': entries_serialized.data
        }

        return Response(
            response_data,
            status=status.HTTP_200_OK
        )




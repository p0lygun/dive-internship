from rest_framework import serializers
from .models import Entry


class EntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Entry
        fields = '__all__'


class EntrySerializerForUser(EntrySerializer, serializers.ModelSerializer):

    class Meta:
        model = Entry
        exclude = ('owner',)


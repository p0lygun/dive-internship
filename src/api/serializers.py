from typing import TYPE_CHECKING
from django.db.models import Q

from rest_framework import serializers
from .models import Entry

if TYPE_CHECKING:
    from accounts.models import CustomUser


class EntrySerializer(serializers.ModelSerializer):
    is_under_total_calories = serializers.SerializerMethodField()

    class Meta:
        model = Entry
        fields = '__all__'

    def get_is_under_total_calories(self, obj: Entry):
        owner: 'CustomUser'
        owner = obj.owner
        if owner is None:
            return False
        same_day_entries = Q(time__day=obj.time.day)
        same_owner = Q(owner=owner)
        entries = Entry.objects.filter(same_owner & same_day_entries)
        total_cals_today = sum(entry.calories for entry in entries)
        return total_cals_today < owner.calories_per_day


class EntrySerializerForUser(EntrySerializer, serializers.ModelSerializer):
    owner = None

    class Meta:
        model = Entry
        exclude = ('owner',)


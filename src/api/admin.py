from django.contrib import admin

from . import models


@admin.register(models.Entry)
class EntryAdminModel(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

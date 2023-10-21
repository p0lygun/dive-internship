from django.urls import path
from .views import EntryItemView

urlpatterns = [
    path('entries/', EntryItemView.as_view(), name='entries-get')
]

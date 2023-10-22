from django.urls import path
from .views import EntryItemView, EntryItemDetailView

urlpatterns = [
    path('entries/', EntryItemView.as_view(), name='entries'),
    path('entries/<str:pk>', EntryItemDetailView.as_view(), name="entry-detail")
]

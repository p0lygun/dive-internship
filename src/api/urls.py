from django.urls import path
from .views import EntryItemView, EntryItemDetailView, UserDetailView, UserView

urlpatterns = [
    path('entries/', EntryItemView.as_view(), name='entries'),
    path('entries/<str:pk>', EntryItemDetailView.as_view(), name="entry-detail"),

    path('users/', UserView.as_view(), name='api-users'),
    path('users/<str:pk>', UserDetailView.as_view(), name='api-users-detail'),
]

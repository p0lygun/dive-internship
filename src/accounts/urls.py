from django.urls import path, include

from .views import SignUpUserView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('signup', SignUpUserView)


urlpatterns = [
    path('', include(router.urls))
]

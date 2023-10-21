from django.urls import path, include

from .views import SignUpUserView, CheckLoginView
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = routers.DefaultRouter()

router.register('signup', SignUpUserView)

urlpatterns = [
    path('', include(router.urls)),

    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/check/', CheckLoginView.as_view(), name='check_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

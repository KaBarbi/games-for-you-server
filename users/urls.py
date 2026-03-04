from django.urls import path
from .views.user_views import MeView
from rest_framework_simplejwt.views import TokenRefreshView
from .views.auth_views import RegisterView, MyTokenObtainPairView, MyTokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path("login/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
    path("me/", MeView.as_view(), name="me"),
]

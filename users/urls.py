from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    UserDetailView,
    UserUpdateView
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("me/", UserDetailView.as_view()),
    path("me/update/", UserUpdateView.as_view()),
]

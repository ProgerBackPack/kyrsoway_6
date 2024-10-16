from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import (
    UserRegisterView,
    email_verification,
    UserDetailView,
    UserUpdateView,
    UserListView,
    toggle_is_active,
)

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("email-confirm/<str:token>", email_verification, name="email_confirm"),
    path("profiles/view", UserListView.as_view(), name="user_view"),
    path("profile/<int:pk>", UserDetailView.as_view(), name="user_detail"),
    path("profile/<int:pk>/update", UserUpdateView.as_view(), name="user_update"),
    path("profile/<int:pk>/confirm-delete", UserUpdateView.as_view(), name="user_delete"),
    path("profile/<int:pk>/activate", toggle_is_active, name="toogle_activate"),
]
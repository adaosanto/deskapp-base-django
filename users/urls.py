from django.urls import path

from .views import CreateUsersView, ListUsersView, LoginView, RegisterView

urlpatterns = [
    path("create/", CreateUsersView.as_view(), name="users-create"),
    path("register/", RegisterView.as_view(), name="users-register"),
    path("", ListUsersView.as_view(), name="users-list"),
    path("login/", LoginView.as_view(), name="login"),
]

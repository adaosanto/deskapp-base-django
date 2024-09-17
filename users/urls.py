from django.urls import path

from projeto.urls import api

from .services.api import router
from .views import (
    CreateUsersView,
    ListUsersView,
    LoginView,
    RegisterView,
    UpdateUsersView,
)

api.add_router("users", router)

urlpatterns = [
    path("create/", CreateUsersView.as_view(), name="users-create"),
    path("<int:pk>/update/", UpdateUsersView.as_view(), name="users-update"),
    path("register/", RegisterView.as_view(), name="users-register"),
    path("", ListUsersView.as_view(), name="users-list"),
    path("login/", LoginView.as_view(), name="login"),
]

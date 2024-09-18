from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from ninja import Router

from .schemas import UserSchema

router = Router()

User = get_user_model()


@router.delete("/", url_name="users-delete")
def delete_user(request, user_id: int):
    user = get_object_or_404(User, pk=user_id)
    user.is_active = False
    return {"message": _("User deleted successfully")}


@router.get("/", response=UserSchema, url_name="users-list")
def get_user(request, user_id: int):
    user = get_object_or_404(User, pk=user_id)
    return user

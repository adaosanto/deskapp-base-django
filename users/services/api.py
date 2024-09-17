from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from ninja import Router

router = Router()

User = get_user_model()


@router.delete("/")
def delete_user(request, user_id: int):
    user = get_object_or_404(User, pk=user_id)
    user.is_active = False
    return {"message": _("User deleted successfully")}

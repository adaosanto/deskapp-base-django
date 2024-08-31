from django.db import models
from django.utils.translation import gettext_lazy as _


class City(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    description = models.TextField(_("Description"), max_length=1000, blank=True)

    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    def __str__(self) -> str:
        return self.name

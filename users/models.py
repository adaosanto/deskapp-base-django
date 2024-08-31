import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from stdimage import StdImageField

from categorys.models import Category
from cities.models import City


def get_file_path(_instance, filename):
    """Function to get file path and generate unique name"""
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return filename


class CustomUserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The given email must be set"))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        """
        Create common user
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        """
        Create super user
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    PERSON_TYPES = (("P", _("Person")), ("C", _("Company")))

    email = models.EmailField(_("email address"), unique=True)
    full_name = models.CharField(_("full name"), max_length=120, null=True)
    document_number = models.CharField(_("document number"), max_length=14, null=True)
    person_type = models.CharField(
        _("person type"), max_length=2, choices=PERSON_TYPES, null=True
    )
    city = models.ForeignKey(
        City, on_delete=models.PROTECT, blank=False, null=True, verbose_name=_("city")
    )
    cellphone = models.CharField(_("cellphone"), max_length=15, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        blank=False,
        null=True,
        verbose_name=_("Category"),
    )
    image_profile = StdImageField(
        _("Image Profile"),
        upload_to=get_file_path,
        default=None,
        variations={"thumb": {"width": 512, "height": 512, "crop": True}},
        delete_orphans=True,
    )
    # Add other fields as needed
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    last_login = models.DateTimeField(_("last login"), blank=True, null=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def get_absolute_url(self):
        return reverse_lazy("users:detail", kwargs={"pk": self.pk})

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name or self.email.split("@")[0]

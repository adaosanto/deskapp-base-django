import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UsernameField,
)
from django.utils.translation import gettext_lazy as _
from validate_docbr import CNPJ, CPF

User = get_user_model()


class CustomStyleMixin:
    """Mixin to apply common styles and attributes to form fields."""

    exclude_fields = []

    def apply_common_styles(self):
        for field_name, field in self.fields.items():
            if field_name not in self.exclude_fields:
                field.widget.attrs.setdefault("class", "form-control")
        # self.fields["email"].widget.attrs.update(
        #     {
        #         "onblur": "validateEmail(this)",
        #         "autofocus": False,
        #     }
        # )
        # self.fields["cellphone"].widget.attrs["onblur"] = "validateCellphone(this)"
        # self.fields["full_name"].widget.attrs["onblur"] = "validateName(this)"
        # self.fields["document_number"].widget.attrs["onblur"] = "validateDoc(this)"
        # self.fields["person_type"].widget.attrs.update(
        #     {
        #         "class": "custom-select2 form-control",
        #     }
        # )
        # self.fields["city"].widget.attrs.update(
        #     {
        #         "class": "custom-select2 form-control",
        #         "onblur": "validateRequired(this, '%s')" % _("city"),
        #     }
        # )
        # self.fields["category"].widget.attrs.update(
        #     {
        #         "class": "custom-select2 form-control",
        #         "onblur": "validateRequired(this, '%s')" % _("category"),
        #     }
        # )
        # self.fields["password1"].widget.attrs["onblur"] = "validatePassword(this)"
        # self.fields["password2"].widget.attrs[
        #     "onblur"
        # ] = "validateConfirmPassword(this)"
        # self.fields["groups"].widget.attrs.update(
        #     {"class": "custom-select2 form-control"}
        # )


class BaseUserValidationMixin(object):
    def clean_cellphone(self):
        cellphone = self.cleaned_data.get("cellphone")
        if cellphone:
            cleaned_cellphone = re.sub(r"\D", "", cellphone)
            if len(cleaned_cellphone) < 10 or len(cleaned_cellphone) > 11:
                raise forms.ValidationError(
                    _("Phone number must have 10 or 11 digits.")
                )
            return cleaned_cellphone
        raise forms.ValidationError(_("This field is required."))

    def clean_document_number(self):
        document_number = self.cleaned_data.get("document_number")

        if not document_number:
            raise forms.ValidationError(_("This field is required."))

        cleaned_document_number = re.sub(r"\D", "", document_number)

        if len(cleaned_document_number) <= 11:
            validator = CPF()
        else:
            validator = CNPJ()

        if not validator.validate(cleaned_document_number):
            raise forms.ValidationError(_("Document invalid."))

        return cleaned_document_number

    def clean_person_type(self):
        person_type = self.cleaned_data.get("person_type")
        document_number = self.cleaned_data.get("document_number")

        if not person_type:
            raise forms.ValidationError(_("This field is required."))
        if len(document_number) <= 11:
            person_type = "P"
        else:
            person_type = "C"

        return person_type


class UserLoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "E-mail",
                "id": "email",
            }
        )
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "**********",
            }
        ),
    )

    error_messages = {
        "invalid_login": _("Please enter a correct email and password."),
        "inactive": _("Account is inactive."),
    }


class CustomUserCreationForm(
    CustomStyleMixin, BaseUserValidationMixin, UserCreationForm
):
    usable_password = None

    class Meta:
        model = User
        fields = [
            "full_name",
            "email",
            "cellphone",
            "document_number",
            "person_type",
            "city",
            "category",
            "password1",
            "password2",
            "groups",
            "image_profile",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_common_styles()

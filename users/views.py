from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from utils.views import BasePaginator, LoginRequiredMixin, TemplateView

from .forms import CustomUserCreationForm, UserCustomUpdateForm, UserLoginForm


class LoginView(LoginView):
    template_name = "users/login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("admin")
    form_class = UserLoginForm

    def form_invalid(self, form: UserLoginForm):
        errors = form.errors.values()
        for error in errors:
            messages.error(self.request, error)
        return super().form_invalid(form)


class ListUsersView(LoginRequiredMixin, BasePaginator):
    template_name = "users/list_users.html"
    model = get_user_model()
    fields = ["id", "full_name", "document_number", "email", "cellphone", "city.name"]


class UpdateUsersView(LoginRequiredMixin, UpdateView):
    template_name = "users/update_user.html"
    model = get_user_model()
    form_class = UserCustomUpdateForm


class CreateUsersView(LoginRequiredMixin, CreateView):
    template_name = "users/create_user.html"
    form_class = CustomUserCreationForm


class RegisterView(TemplateView):
    template_name = "users/register.html"

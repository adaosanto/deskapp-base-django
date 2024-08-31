from django.views.generic import TemplateView

from utils.views import LoginRequiredMixin


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home/index.html"

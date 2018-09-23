from django.views.generic import CreateView
from django.urls import reverse

from .forms import RegisterForm


class RegisterView(CreateView):
    template_name = 'user/register.html'
    form_class = RegisterForm

    def get_success_url(self):
        return reverse('user:login')

from django.views.generic import TemplateView
from django.urls import reverse
from django.http import HttpResponseRedirect


class WelcomeView(TemplateView):
    template_name = 'welcome/welcome.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(
                reverse('dashboard:dashboard'))

        return super().get(request, *args, **kwargs)

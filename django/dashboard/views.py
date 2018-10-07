from datetime import datetime

from core.models import Action
from dashboard.forms import ChooseDate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.utils.timezone import get_current_timezone
from django.views.generic import ListView


class DashboardView(LoginRequiredMixin, ListView):
    template_name = 'dashboard/dashboard.html'

    def get_queryset(self):
        dt = self.get_date()

        if dt is None:
            dt = timezone.now()

        qs = Action.dashboard.get(
            user=self.request.user,
            day=dt.day,
            month=dt.month,
            year=dt.year
        )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx.update({'form': ChooseDate(initial={
            'date': self.get_date()
        })})

        return ctx

    def get_date(self):
        params = self.request.GET.dict()
        tz = get_current_timezone()

        try:
            dt = tz.localize(
                datetime.strptime(params.get('date'), '%Y-%m-%d'))
        except (TypeError, ValueError):
            dt = None

        return dt

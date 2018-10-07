from calendar import monthrange
from datetime import date, timedelta

from core.models import Action
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.utils import timezone
from django.views.generic import RedirectView, TemplateView


class ActionCurrentMonthView(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        today = timezone.now()
        return reverse(
            'statistic:month',
            kwargs={
                'month': today.month,
                'year': today.year,
                'pk': self.get_action()
            }
        )

    def get_action(self):
        return self.kwargs['pk']


class ActionMonthView(LoginRequiredMixin, TemplateView):
    template_name = 'statistic/month.html'

    def dispatch(self, *args, **kwargs):
        user = Action.objects.filter(id=self.get_action()).first().user

        if user != self.request.user:
            raise PermissionDenied

        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # Month statistic
        ctx.update({
            'list': Action.month_statistic.get(
                id=self.get_action(),
                user=self.request.user,
                month=self.get_month(),
                year=self.get_year()
            )
        })

        # Dates
        ctx.update({
            'monthrange': [
                i for i in range(1, monthrange(2018, 10)[1] + 1)
            ],
            'previous_month': self.get_previous_month(),
            'next_month': self.get_next_month(),
            'chosen_date': self.get_chosen_date()
        })

        return ctx

    def get_month(self):
        return self.kwargs['month']

    def get_year(self):
        return self.kwargs['year']

    def get_action(self):
        return self.kwargs['pk']

    def get_chosen_date(self):
        chosen_date = date(self.get_year(), self.get_month(), 1)
        return chosen_date

    def get_today(self):
        today = date.today().replace(day=1)
        return today

    def get_previous_month(self):
        chosen_date = self.get_chosen_date()

        previous_month = (
            chosen_date.replace(day=1) - timedelta(1)).replace(day=1)

        date_of_creation_action = Action.objects.filter(
            pk=self.get_action()
        ).first().created.date()

        if date_of_creation_action >= chosen_date:
            previous_month = None

        return previous_month

    def get_next_month(self):
        today = self.get_today()
        chosen_date = self.get_chosen_date()

        next_month = (
            chosen_date.replace(day=28) + timedelta(10)).replace(day=1)

        if today <= chosen_date:
            next_month = None

        return next_month

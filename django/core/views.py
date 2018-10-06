from calendar import monthrange
from datetime import date, datetime, timedelta

from core.forms import ChooseDate, RecordCreate
from core.models import Action, Record
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseBadRequest
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import get_current_timezone
from django.views.generic import (CreateView, ListView, RedirectView,
                                  TemplateView, UpdateView)


class DashBoardView(LoginRequiredMixin, ListView):
    template_name = 'core/dashboard.html'

    def get_queryset(self):
        dt = self.get_date()

        if dt is None:
            dt = timezone.now()

        qs = Action.objects.dashboard(
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


class RecordListView(LoginRequiredMixin, ListView):
    paginate_by = 10

    def get_queryset(self):
        qs = Record.objects.filter(
            action__user=self.request.user
        )
        return qs


class RecordCreateView(LoginRequiredMixin, CreateView):
    model = Record
    form_class = RecordCreate

    def form_valid(self, form):
        self.object = form.save(commit=False)

        if self.object.action.user != self.request.user:
            return HttpResponseBadRequest()

        self.object.save()

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(RecordCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('core:record-list')


class ActionListView(LoginRequiredMixin, ListView):
    paginate_by = 10

    def get_queryset(self):
        qs = Action.objects.filter(
            user=self.request.user
        )
        return qs


class ActionCreateView(LoginRequiredMixin, CreateView):
    model = Action
    fields = ('text', 'color', 'unit')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user

        self.object.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('core:action-list')


class ActionUpdateView(LoginRequiredMixin, UpdateView):
    model = Action
    fields = ('text', 'color', 'unit')

    def dispatch(self, *args, **kwargs):
        user = self.get_object().user

        if user != self.request.user:
            raise PermissionDenied

        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('core:dashboard')


class ActionCurrentMonthView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        today = timezone.now()
        return reverse(
            'core:action-month',
            kwargs={
                'month': today.month,
                'year': today.year,
                'pk': self.get_action()
            }
        )

    def get_action(self):
        return self.kwargs['pk']


class ActionMonthView(LoginRequiredMixin, TemplateView):
    template_name = 'core/action_month.html'

    def dispatch(self, *args, **kwargs):
        user = Action.objects.filter(id=self.get_action()).first().user

        if user != self.request.user:
            raise PermissionDenied

        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        chosen_date = date(self.get_year(), self.get_month(), 1)
        today = date.today().replace(day=1)

        previous_month = (
            chosen_date.replace(day=1) - timedelta(1)).replace(day=1)
        next_month = (
            chosen_date.replace(day=28) + timedelta(10)).replace(day=1)

        date_of_creation_action = Action.objects.filter(
            pk=self.get_action()
        ).first().created.date()

        if date_of_creation_action >= chosen_date:
            previous_month = None

        if today <= chosen_date:
            next_month = None

        ctx.update({
            'list': Action.objects.get_month_statistic(
                id=self.get_action(),
                user=self.request.user,
                month=self.get_month(),
                year=self.get_year()
            ),
            'monthrange': [
                i for i in range(1, monthrange(2018, 10)[1] + 1)
            ],
            'previous_month': previous_month,
            'next_month': next_month,
            'chosen_date': chosen_date
        })

        return ctx

    def get_month(self):
        return self.kwargs['month']

    def get_year(self):
        return self.kwargs['year']

    def get_action(self):
        return self.kwargs['pk']

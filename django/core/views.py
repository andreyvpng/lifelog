from datetime import datetime

from core.forms import RecordCreate
from core.models import Action, Record
from core.permissions import IsOwnerOfAction
from core.serializers import ActionSerializer, RecordSerializer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.timezone import get_current_timezone
from django.views.generic import (CreateView, DeleteView, ListView,
                                  TemplateView, UpdateView)
from rest_framework import permissions, viewsets


class WelcomeView(TemplateView):
    template_name = 'core/welcome.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(
                reverse('dashboard:dashboard'))

        return super().get(request, *args, **kwargs)


class ActionUpdateView(LoginRequiredMixin, UpdateView):
    model = Action
    fields = ('text', 'color', 'unit')

    def dispatch(self, *args, **kwargs):
        user = self.get_object().user

        if user != self.request.user:
            raise PermissionDenied

        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('dashboard:dashboard')


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

    def get_initial(self):
        initial = super(RecordCreateView, self).get_initial()
        initial['action'] = self.get_action()
        return initial

    def get_form_kwargs(self):
        kwargs = super(RecordCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('dashboard:dashboard')

    def get_action(self):
        params = self.request.GET.dict()
        action = params.get('action')

        if not Action.objects.filter(id=action):
            action = None

        return action


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
        return reverse('dashboard:dashboard')


class ActionDeleteView(LoginRequiredMixin, DeleteView):
    model = Action
    success_url = reverse_lazy('dashboard:dashboard')

    def dispatch(self, *args, **kwargs):
        user = self.get_object().user

        if user != self.request.user:
            raise PermissionDenied

        return super().dispatch(*args, **kwargs)


class ActionViewSet(viewsets.ModelViewSet):
    queryset = Action.dashboard
    serializer_class = ActionSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.BasePermission
    )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        dt = self.get_date()

        if dt is None:
            dt = timezone.now()

        qs = self.queryset.get(
            user=self.request.user,
            day=dt.day,
            month=dt.month,
            year=dt.year
        )
        return qs

    def get_date(self):
        params = self.request.GET.dict()
        tz = get_current_timezone()

        try:
            dt = tz.localize(
                datetime.strptime(params.get('date'), '%Y-%m-%d'))
        except (TypeError, ValueError):
            dt = None

        return dt


class RecordCreateAPIView(viewsets.ModelViewSet):
    queryset = Record.objects
    serializer_class = RecordSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOfAction,
    )

    def get_queryset(self):
        qs = self.queryset.filter(
            action__user=self.request.user,
        )
        return qs

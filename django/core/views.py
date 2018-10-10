from core.forms import RecordCreate
from core.models import Action, Record
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.http.response import HttpResponseBadRequest
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, ListView,
                                  TemplateView, UpdateView)


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
        return reverse('core:dashboard')


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

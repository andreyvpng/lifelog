from core.models import Action
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from goal.forms import GoalForm
from goal.models import Goal


class GoalCreateView(LoginRequiredMixin, CreateView):
    form_class = GoalForm
    template_name = 'goal/goal_form.html'

    def dispatch(self, *args, **kwargs):
        action = self.get_action()
        is_goal_exist = Goal.objects.filter(action=action)

        if is_goal_exist:
            return HttpResponseRedirect(reverse('goal:update', kwargs={
                'pk': self.kwargs['pk']}))

        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.action = self.get_action()

        if self.object.action.user != self.request.user:
            return HttpResponseBadRequest()

        self.object.save()
        return super().form_valid(form)

    def get_action(self):
        return Action.objects.get(id=self.kwargs['pk'])

    def get_success_url(self):
        return reverse('dashboard:dashboard')


class GoalUpdateView(LoginRequiredMixin, UpdateView):
    form_class = GoalForm
    template_name = 'goal/goal_form.html'

    def dispatch(self, *args, **kwargs):
        goal = self.get_object()

        if goal.action.user != self.request.user:
            raise PermissionDenied

        return super().dispatch(*args, **kwargs)

    def get_object(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        object = get_object_or_404(Goal, action=pk)
        return object

    def get_success_url(self):
        return reverse('dashboard:dashboard')

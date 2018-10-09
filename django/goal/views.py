from core.models import Action
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import FormView
from goal.forms import GoalCreate
from goal.models import Goal


class GoalCreateUpdateView(PermissionDenied, FormView):
    form_class = GoalCreate
    template_name = 'goal/goal_form.html'

    def get_initial(self):
        initial = super(GoalCreateUpdateView, self).get_initial()
        initial['action'] = self.get_action()
        return initial

    def get_form_kwargs(self):
        kwargs = super(GoalCreateUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        action = form.cleaned_data['action']
        goal = Goal.objects.filter(action=action)
        if goal:
            goal.update(**form.cleaned_data)
        else:
            Goal.objects.create(**form.cleaned_data)
        return HttpResponseRedirect(self.get_success_url())

    def get_action(self):
        params = self.request.GET.dict()
        action = params.get('action')

        if not Action.objects.filter(id=action):
            action = None

        return action

    def get_success_url(self):
        return reverse('dashboard:dashboard')

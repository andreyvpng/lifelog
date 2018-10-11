from core.models import Action
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseBadRequest
from django.urls import reverse
from django.views.generic import UpdateView
from goal.forms import GoalCreate
from goal.models import Goal


class GoalCreateUpdateView(PermissionDenied, UpdateView):
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
        self.object = form.save(commit=False)

        if self.object.action.user != self.request.user:
            return HttpResponseBadRequest()

        self.object.save()

        return super().form_valid(form)

    def get_object(self, queryset=None):

        # get the existing object or created a new one
        obj, created = Goal.objects.get_or_create(action=self.get_action())

        return obj

    def get_action(self):
        params = self.request.GET.dict()
        action = params.get('action')

        if not Action.objects.filter(id=action):
            action = None

        return action

    def get_success_url(self):
        return reverse('dashboard:dashboard')

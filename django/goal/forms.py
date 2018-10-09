from core.models import Action
from django import forms
from goal.models import Goal


class GoalCreate(forms.ModelForm):

    class Meta:
        model = Goal
        fields = ('action', 'daily_value')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['action'].queryset =\
            Action.objects.filter(user=user)

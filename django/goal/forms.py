from django import forms
from goal.models import Goal


class GoalForm(forms.ModelForm):

    class Meta:
        model = Goal
        fields = ('daily_value', )

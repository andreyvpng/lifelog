from core.models import Action, Record
from django import forms


class RecordCreate(forms.ModelForm):

    class Meta:
        model = Record
        fields = ('action', 'value')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['action'].queryset =\
            Action.objects.filter(user=user)


class ChooseDate(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
        'id': 'datepicker',
        'onchange': 'this.form.submit()'
    }), label='')

from django import forms


class ChooseDate(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
        'id': 'datepicker',
        'onchange': 'this.form.submit()'
    }), label='')

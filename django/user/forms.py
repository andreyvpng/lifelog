from user.models import User

from django.contrib.auth.forms import (UserChangeForm, UserCreationForm,
                                       UsernameField)


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}


class UserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')


class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = UserChangeForm.Meta.fields

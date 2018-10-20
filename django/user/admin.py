from user.forms import UserChangeForm, UserCreationForm
from user.models import User

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ['username']


admin.site.register(User, CustomUserAdmin)

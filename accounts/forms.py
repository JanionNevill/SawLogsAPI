from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm

from accounts.models import CustomUser


class CustomUserCreationForm(AdminUserCreationForm):
    model = CustomUser
    fields = ("username", "email")


class CustomUserChangeForm(UserChangeForm):
    model = CustomUser
    fields = ("username", "email")

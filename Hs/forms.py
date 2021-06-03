from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User


class AddKeywordForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField()

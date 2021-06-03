from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User


class KeywordForm(forms.Form):
    name = forms.CharField(label='名称')
    description = forms.CharField(label='描述', max_length=200)

    initial = {
        'name': '请输入名称',
        'description': '请输入描述'
    }

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import Form, ModelForm

from .models import Account, Team


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = Account
        fields = ('username', 'email', 'password1', 'password2',)


class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ['name']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=10)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

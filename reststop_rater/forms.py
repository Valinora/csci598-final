from django import forms
from django.contrib.auth.models import User

class JoinForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(widget=forms.EmailInput())
    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

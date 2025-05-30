from django import forms
from django.contrib.auth.models import User

from .models.bathroom import Bathroom
from .models.review import Review

class JoinForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ("username", "email", "password")

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class CreateBathroomForm(forms.ModelForm):
    class Meta:
        model = Bathroom
        exclude = ("rating",)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

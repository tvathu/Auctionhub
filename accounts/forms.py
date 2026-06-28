from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=[('buyer', 'Buyer'), ('seller', 'Seller')])

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']
from django import forms
from django.contrib.auth.models import User
from django.core.validators import URLValidator, validate_email, ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(label='Email', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))


def email_not_taken(email):
    if User.objects.filter(username=email):
        raise ValidationError('Ten email jest zajęty!')


class RegisterForm(forms.Form):
    first_name = forms.CharField(label='Imię', widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    last_name = forms.CharField(label='Nazwisko', widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
    email = forms.CharField(label='Email', validators=[email_not_taken], widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(label='Hasło', widget= forms.PasswordInput(attrs={'placeholder': 'Hasło'}))
    password2 = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput(attrs={'placeholder': 'Powrtórz hasło'}))

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password1'] != cleaned_data['password2']:
            raise ValidateError('Hasła różnią się od siebie!')
        return cleaned_data

from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CareTraceAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "autocomplete": "username", "placeholder": "Username"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "autocomplete": "current-password", "placeholder": "Password"}
        )
    )


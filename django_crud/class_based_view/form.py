from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "form-control form-control-lg", "id": "old_password", "placeholder": "Enter your password"}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "form-control form-control-lg", "id": "password1", "placeholder": "Enter your new password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "form-control form-control-lg", "id": "password2", "placeholder": "Confirm your password"}))

    class Meta:
        model = User
        fields = ["old_password", "new_password1", "old_password1"]


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control form-control-lg", "id": "username", "placeholder": "Enter username"}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "form-control form-control-lg", "id": "password", "placeholder": "Enter password"}))

    class Meta:
        model = User
        fields = ["username", "password"]

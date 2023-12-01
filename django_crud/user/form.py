from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ProfileForm(forms.ModelForm):
    phonenumber = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Enter phone number"}))
    address = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Enter address"}))
    proffession = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Enter address"}))

    class Meta:
        model = models.Profile
        fields = ["address", "proffession", "phonenumber"]


class UserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={"class": "form-control form-control-lg", "id": "email", "placeholder": "Enter email", "name": "email"}), validators=[])
    username = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control form-control-lg", "id": "username", "placeholder": "Enter username"}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "form-control form-control-lg", "id": "password1", "placeholder": "Enter password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "form-control form-control-lg", "id": "password2", "placeholder": "confirm password"}))

    class Meta:
        model = User
        fields = ["email", "username", "password1", "password2"]

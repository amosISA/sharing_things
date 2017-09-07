# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# class RegisterForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = [
#             "username",
#             "first_name",
#             "last_name",
#             "email"
#         ]
#
#         labels = {
#             "username": "Nombre de usuario",
#             "first_name": "Nombre",
#             "last_name": "Apellidos",
#             "email": "E-mail"
#         }
#
#     # def clean_email(self):
#     #     email = self.cleaned_data.get("email")
#     #     if ".edu" in email:
#     #         raise forms.ValidationError("NADA DE NADA")
#     #     return email
#
#     def clean_email(self):
#         email = self.cleaned_data.get("email")
#         qs = User.objects.filter(email__iexact=email)
#         if qs.exists:
#             raise forms.ValidationError("El email {} ya está en uso.".format(email))
#         return email

class RegisterForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False
        # create a new user hash for activating email.

        if commit:
            user.save()
        return user
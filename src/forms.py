# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email"
        ]

        labels = {
            "username": "Nombre de usuario",
            "first_name": "Nombre",
            "last_name": "Apellidos",
            "email": "E-mail"
        }

    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     if ".edu" in email:
    #         raise forms.ValidationError("NADA DE NADA")
    #     return email

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email__iexact=email)
        if qs.exists:
            raise forms.ValidationError("El email {} ya está en uso.".format(email))
        return email
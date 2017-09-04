# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView

# Create your views here.
User = get_user_model()

class ProfileDetailView(DetailView):
    queryset = User.objects.all().filter(is_active=True)
    template_name = 'profiles/profile.html'

    def get_object(self):
        username = self.kwargs.get("username")

        if username is None:
            raise Http404
        return get_object_or_404(User, username__iexact=username, is_active=True)
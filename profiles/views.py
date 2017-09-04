# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView

from posts.models import Post

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

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(*args, **kwargs)
        user = context['user']
        query = self.request.GET.get('q')
        qs = Post.objects.filter(user=user).search(query)
        #if query:
            #qs = qs.search(query) # aqui como se le pasa el usuario busca solo los posts de ese usuario
            #qs = Post.objects.search(query) # aqui como no hay usuario, busca en todos los posts
        if qs.exists():
            context['settings'] = qs
        return context
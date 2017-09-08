# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, View

from posts.models import Post
from .models import Profile

# Create your views here.
User = get_user_model()

# Button for following users
class ProfileFollowToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        username_to_toggle = request.POST.get("username")
        profile_, is_following = Profile.objects.toggle_follow(request.user, username_to_toggle)
        return redirect("/profile/{}/".format(profile_.user.username))

# User Profile
class ProfileDetailView(LoginRequiredMixin, DetailView):
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

        is_following=False
        if user.profile in self.request.user.is_following.all():
            is_following=True
        context['is_following'] = is_following
        query = self.request.GET.get('q')
        qs = Post.objects.filter(user=user).search(query)
        #if query:
            #qs = qs.search(query) # aqui como se le pasa el usuario busca solo los posts de ese usuario
            #qs = Post.objects.search(query) # aqui como no hay usuario, busca en todos los posts
        if qs.exists():
            context['settings'] = qs
        return context

# User activation email
def activate_user_view(request, code=None, *args, **kwargs):
    if code:
        qs = Profile.objects.filter(activation_key=code)
        if qs.exists() and qs.count() == 1:
            profile = qs.first()
            if not profile.activated:
                user_ = profile.user
                user_.is_active = True
                user_.save()
                profile.activated = True
                profile.activation_key = None
                profile.save()
                return redirect("login")
    # invalid code
    return redirect("login")

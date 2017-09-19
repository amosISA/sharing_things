from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render

from django.views.generic import CreateView
from django.contrib.auth.views import login
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from .forms import RegisterForm
from django.contrib.auth.views import login

User = get_user_model()

def src_index(request):
    return HttpResponseRedirect(reverse('posts:index'))

# --------------- User Registration --------------- #
class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "register.html"
    success_url = reverse_lazy("posts:index")

    # if user is logged, redirect him
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('posts:index'))
        return super(RegisterView, self).dispatch(*args, **kwargs)

# --------------- Login --------------- #
# def custom_login(request):
#     if request.user.is_authenticated():
#         return HttpResponseRedirect(reverse('posts:index'))
#     else:
#         return login(request, template_name='login.html')

def custom_login(request, *args, **kwargs):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('posts:index'))
    else:
        return login(request, template_name='login.html')
    return login(request, *args, **kwargs)

# --------------- Update User Information --------------- #
class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'user_update.html'
    fields = ['username', 'email', 'first_name', 'last_name']

    def get_success_url(self):
        return reverse('profiles:user_profile', kwargs={'username': self.request.user})

    def get_object(self, queryset=None):
        '''This method will load the object
           that will be used to load the form
           that will be edited'''
        return self.request.user

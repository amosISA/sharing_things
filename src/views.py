from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render

from django.views.generic import CreateView
from django.contrib.auth.views import login

from .forms import RegisterForm, LoginForm
from django.contrib.auth.views import login

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

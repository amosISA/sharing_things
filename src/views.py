from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy

from django.contrib.auth.models import User

from django.views.generic import CreateView
from django.contrib.auth.views import login

from .forms import RegisterForm

def src_index(request):
    return HttpResponseRedirect(reverse('posts:index'))

# --------------- User Registration --------------- #
class RegisterUser(CreateView):
    model = User
    template_name = "register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("posts:index")

# --------------- Login --------------- #
def custom_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('posts:index'))
    else:
        return login(request, template_name='login.html')
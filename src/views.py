from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import CreateView

from .forms import RegisterForm

def src_index(request):
    return HttpResponseRedirect(reverse('posts:index'))

# --------------- User Registration --------------- #
class RegisterUser(CreateView):
    model = User
    template_name = "register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("posts:index")
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def src_index(request):
    return HttpResponseRedirect(reverse('posts:index'))
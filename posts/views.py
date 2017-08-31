# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Post
from .forms import PostForm

#--------------------------------------------------------------------#
##------------------------- FUNCTION-BASED VIEWS ---------------------##
#--------------------------------------------------------------------#

# --------------- List All Posts --------------- #
def index(request):
    queryset_list = Post.objects.all() #.order_by("-created")
    paginator = Paginator(queryset_list, 3)  # Show 3 posts per page

    queryset = request.GET.get('page')
    try:
        queryset = paginator.page(queryset)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        'object_list': queryset,
        'user': request.user
    }
    return render(request, 'posts/index.html', context)

# --------------- Get Post By Id --------------- #
def getPostById(request, id=None):
    instance = get_object_or_404(Post, id=id)
    context = {
        'instance': instance
    }
    return render(request, 'posts/post_detail.html', context)

# --------------- Get Post By Slug --------------- #
def getPostBySlug(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    context = {
        'instance': instance
    }
    return render(request, 'posts/post_detail.html', context)

# --------------- Create New Post --------------- #
def newPost(request):
    if request.user.is_authenticated():
        form = PostForm(request.POST or None, request.FILES or None)
        if request.method == "POST":
            if form.is_valid():
                # Create, but don't save the new post instance.
                instance = form.save(commit=False)
                instance.user = request.user
                # Save the new instance.
                instance.save()
                # Flash message
                messages.success(request, "Post successfully created.")
                # Redirect
                return HttpResponseRedirect(instance.get_absolute_url())
            else:
                messages.error(request, "Error creating post.")
        context = {
            "form": form
        }
        return render(request, 'posts/post_create.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))

# --------------- Edit Post --------------- #
def editPost(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)

    if request.method == "POST":
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "Post successfully saved.")
            return HttpResponseRedirect(instance.get_absolute_url())
        else:
            messages.error(request, "Error saving the post.")

    context = {
        "instance": instance,
        "form": form
    }
    return render(request, 'posts/post_create.html', context)

# --------------- Delete Post --------------- #
def deletePost(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    image = instance.image
    if image:
        image.delete(save=False)
    instance.delete()
    messages.success(request, "Post successfully deleted.")
    return HttpResponseRedirect(reverse('posts:index'))


#--------------------------------------------------------------------#
##------------------------- CLASS-BASED VIEWS ---------------------##
#--------------------------------------------------------------------#

# --------------- List All Posts --------------- #
class PostListView(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        queryset = Post.objects.all()
        paginator = Paginator(queryset, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            query_set = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            query_set = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            query_set = paginator.page(paginator.num_pages)

        context['object_list'] = query_set
        return context


# --------------- Get Post By Slug --------------- #
class PostDetailView(DetailView):
    context_object_name = 'instance'
    queryset = Post.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        return context

# --------------- Create New Post --------------- #
class PostCreateView(CreateView):
    model = Post
    template_name = 'posts/post_create.html'
    fields = ['title', 'content', 'image']
    success_url = reverse_lazy('posts:index')

# --------------- Edit Post --------------- #
class PostUpdateView(UpdateView):
    model = Post
    template_name = 'posts/post_create.html'
    fields = ['title', 'content', 'image']
    success_url = reverse_lazy('posts:index')

# --------------- Delete Post --------------- #
class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('posts:index')

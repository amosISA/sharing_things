# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post
from .forms import PostForm

# --------------- List All Posts --------------- #
def index(request):
    queryset_list = Post.objects.all() #.order_by("-created")
    paginator = Paginator(queryset_list, 3)  # Show 25 posts per page

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
        'object_list': queryset
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
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            # Create, but don't save the new post instance.
            instance = form.save(commit=False)
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
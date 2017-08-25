# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from .models import Post
from .forms import PostForm

# Create your views here.
def index(request):
    return render(request, 'posts/base.html', {})

# --------------- List All Posts --------------- #
def getAllPosts(request):
    queryset = Post.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, 'posts/base.html', context)

# --------------- Get Post By ID --------------- #
def getPostById(request, id=None):
    instance = get_object_or_404(Post, id=id)
    context = {
        'instance': instance
    }
    return render(request, 'posts/post_detail.html', context)

# --------------- Create New Post --------------- #
def newPost(request):
    form = PostForm(request.POST or None)
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
def editPost(request, id=None):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, instance=instance)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Post successfully saved.")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.success(request, "Error saving the post.")

    context = {
        "instance": instance,
        "form": form
    }
    return render(request, 'posts/post_create.html', context)

# --------------- Delete Post --------------- #
def deletePost(request, id=None):
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "Post successfully deleted.")
    return HttpResponseRedirect(reverse('posts:list_posts'))
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Post
from .forms import PostForm

# Create your views here.
def index(request):
    return render(request, 'posts/index.html', {})

def getAllPosts(request):
    queryset = Post.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, 'posts/index.html', context)

def getPostById(request, id=None):
    instance = get_object_or_404(Post, id=id)
    context = {
        'instance': instance
    }
    return render(request, 'posts/post_detail.html', context)

def newPost(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        # Create, but don't save the new post instance.
        instance = form.save(commit=False)
        # Save the new instance.
        instance.save()
    context = {
        "form": form
    }
    return render(request, 'posts/post_create.html', context)

def editPost(request, id=None):
    instance = get_object_or_404(Post, id=id)

    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)

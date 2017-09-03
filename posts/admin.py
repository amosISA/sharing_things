# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated', 'created', 'user')
    search_fields = ('title', 'content')
    list_filter = ('updated', 'created')
    ordering = ('-created',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'updated', 'created', 'user')
    search_fields = ('post', 'user')
    list_filter = ('updated', 'created')
    ordering = ('-created',)

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
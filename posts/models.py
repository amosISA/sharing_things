# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        ordering = ["title"]
        verbose_name_plural = 'Posts'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail_post", kwargs={"id": self.id})
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
def upload_location(instance, filename):
    first_word = instance.title.split(' ', 1)[0]
    return "posts/%s_%s" % (first_word, filename)

class Post(models.Model):
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True,
                              height_field="height_field",
                              width_field="width_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        ordering = ["-created", "-updated"]
        verbose_name_plural = 'Posts'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail_post", kwargs={"id": self.id})

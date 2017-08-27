# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save

from django.utils.text import slugify

# Create your models here.
def upload_location(instance, filename):
    first_word = instance.title.split(' ', 1)[0]
    return "posts/%s_%s" % (first_word, filename)

class Post(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
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
        return reverse("posts:detail_post", kwargs={"slug": self.slug})


def create_slug(instance, new_slug=None):
    # Lo q slugify hace es si el titulo es: coche item 1
    # Lo devuelve como (con los guiones): tesla-item-1
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug

    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def create_simple_slug(instance):
    slug=slugify(instance.title)
    qs = Post.objects.filter(slug__startswith=slug).order_by("-id")
    if qs.exists():
        return "%s-%s" % (slug, qs.first().id)
    return slug

# Function that do something before the model is saved => save()
def pre_save_post_receiver(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.title)

pre_save.connect(pre_save_post_receiver, sender=Post)
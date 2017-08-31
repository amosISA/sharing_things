# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save

from .utils import unique_slug_generator
from .validators import validate_title

User = settings.AUTH_USER_MODEL

# Create your models here.
def upload_location(instance, filename):
    first_word = instance.title.split(' ', 1)[0]
    return "posts/%s_%s" % (first_word, filename)

class Post(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=120, validators=[validate_title])
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True,
                              height_field="height_field",
                              width_field="width_field")
    height_field = models.IntegerField(default=0, blank=True, null=True)
    width_field = models.IntegerField(default=0, blank=True, null=True)
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

    # Override save function so that I can delete images when they are UPDATED
    def save(self, *args, **kwargs):
        # Delete old file when replacing by updating the file
        try:
            this = Post.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except: pass # When new photo then we do nothing, normal case
        super(Post, self).save(*args, **kwargs)

# Function that do something before the model is saved => save()
def pre_save_post_receiver(sender, instance, *args, **kwargs):
    # Lo q slugify hace es si el titulo es: coche item 1
    # Lo devuelve como (con los guiones): tesla-item-1
    #instance.slug = slugify(instance.title)
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)
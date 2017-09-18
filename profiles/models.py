# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse

from .utils import code_generator
User = settings.AUTH_USER_MODEL

# Create your models here.
def upload_location(instance, filename):
    username = instance.user.username
    return "avatar/%s/%s_%s" % (username,username, filename)

class ProfileManager(models.Manager):
    def toggle_follow(self, request_user, username_to_toggle):
        profile_ = Profile.objects.get(user__username__iexact=username_to_toggle)
        user = request_user
        is_following = False
        if user in profile_.followers.all():
            profile_.followers.remove(user)
        else:
            profile_.followers.add(user)
            is_following = True
        return profile_, is_following

class Profile(models.Model):
    user = models.OneToOneField(User)
    followers = models.ManyToManyField(User, related_name='is_following', blank=True)
    #following = models.ManyToManyField(User, related_name='following', blank=True)
    activation_key = models.CharField(max_length=120, blank=True, null=True)
    activated = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True,
                              height_field="height_field",
                              width_field="width_field")
    height_field = models.IntegerField(default=0, blank=True, null=True)
    width_field = models.IntegerField(default=0, blank=True, null=True)

    objects = ProfileManager()

    def __unicode__(self):
        return self.user.username

    def send_activation_email(self):
        if not self.activated:
            self.activation_key = code_generator()
            self.save()
            path_ = reverse('activate', kwargs={"code": self.activation_key})

            # Send email
            subject = "Activa tu cuenta"
            from_email = settings.DEFAULT_FROM_EMAIL
            message = "Activa tu cuenta aquí: {}".format(path_)
            recipient_list = [self.user.email, ]
            html_message = "<p>Activa tu cuenta aquí: {}</p>".format(path_)
            sent_mail = send_mail(subject,
                                  message,
                                  from_email,
                                  recipient_list,
                                  fail_silently=False,
                                  html_message=html_message)
            return sent_mail

            # Override save function so that I can delete images when they are UPDATED

    def save(self, *args, **kwargs):
        # Delete old file when replacing by updating the file
        try:
            this = Profile.objects.get(id=self.id)
            if this.avatar != self.avatar:
                this.avatar.delete(save=False)
        except:
            pass  # When new photo then we do nothing, normal case
        super(Profile, self).save(*args, **kwargs)

def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        profile, is_created = Profile.objects.get_or_create(user=instance)
        # Hago esto para q cualquier usuario nueva q se registre, yo lo siga de
        # manera automatica
        default_user_profile = Profile.objects.get_or_create(user__id=1)[0] # user__username='amos'
        default_user_profile.followers.add(instance)


post_save.connect(post_save_user_receiver, sender=User)
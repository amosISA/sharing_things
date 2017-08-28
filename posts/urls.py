from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    #url(r'^(?P<id>\d+)/$', views.getPostById, name='detail_post'),
    #url(r'^edit/(?P<id>\d+)/$', views.editPost, name='edit_post'),
    #url(r'^delete/(?P<id>\d+)/$', views.deletePost, name='delete_post'),

    url(r'^new/$', views.newPost, name='new_post'),
    url(r'^(?P<slug>[\w-]+)/$', views.getPostBySlug, name='detail_post'),
    url(r'^edit/(?P<slug>[\w-]+)/$', views.editPost, name='edit_post'),
    url(r'^delete/(?P<slug>[\w-]+)/$', views.deletePost, name='delete_post'),
]
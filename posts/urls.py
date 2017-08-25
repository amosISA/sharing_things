from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^list/$', views.getAllPosts, name='list_posts'),
    url(r'^(?P<id>\d+)/$', views.getPostById, name='detail_post'),
    url(r'^edit/(?P<id>\d+)/$', views.editPost, name='edit_post'),
    url(r'^new/$', views.newPost, name='new_post'),
]
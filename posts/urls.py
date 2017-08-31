from django.conf.urls import url
from . import views

urlpatterns = [
    # --- index ---
    url(r'^$', views.index, name='index'),

    # --- normal urls, with id ---
    #url(r'^(?P<id>\d+)/$', views.getPostById, name='detail_post'),
    #url(r'^edit/(?P<id>\d+)/$', views.editPost, name='edit_post'),
    #url(r'^delete/(?P<id>\d+)/$', views.deletePost, name='delete_post'),

    # --- slug urls ---
    # --- function-based views ---
    url(r'^new/$', views.newPost, name='new_post'),
    #url(r'^new/$', views.PostCreateView.as_view(), name='new_post'),

    url(r'^(?P<slug>[\w-]+)/$', views.getPostBySlug, name='detail_post'),

    url(r'^edit/(?P<slug>[\w-]+)/$', views.editPost, name='edit_post'),
    #url(r'^edit/(?P<slug>[\w-]+)/$', views.PostUpdateView.as_view(), name='edit_post'),

    #url(r'^delete/(?P<slug>[\w-]+)/$', views.deletePost, name='delete_post'),
    url(r'^delete/(?P<slug>[\w-]+)/$', views.PostDeleteView.as_view(), name='delete_post'),

    # --- class-based views ---
    #url(r'^$', views.PostListView.as_view(), name='index'),
    #url(r'^(?P<slug>[\w-]+)/$', views.PostDetailView.as_view(), name='detail_post'),

]
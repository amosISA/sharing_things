from django.conf.urls import url
from django.contrib.auth.views import login, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', login, {'template_name': 'posts/users/login.html'}, name='login'),
    url(r'^register/$', views.RegisterUser.as_view(), name="register"),


    #url(r'^(?P<id>\d+)/$', views.getPostById, name='detail_post'),
    #url(r'^edit/(?P<id>\d+)/$', views.editPost, name='edit_post'),
    #url(r'^delete/(?P<id>\d+)/$', views.deletePost, name='delete_post'),

    url(r'^new/$', views.newPost, name='new_post'),
    url(r'^(?P<slug>[\w-]+)/$', views.getPostBySlug, name='detail_post'),
    url(r'^edit/(?P<slug>[\w-]+)/$', views.editPost, name='edit_post'),
    url(r'^delete/(?P<slug>[\w-]+)/$', views.deletePost, name='delete_post'),

    url(r'^reset/password_reset', password_reset, {"template_name": "posts/users/password_reset_form.html",
        "email_template_name": "posts/users/password_reset_email.html"}, name="password_reset"),
    url(r'^reset/password_reset_done', password_reset_done, {"template_name":"posts/users/password_reset_done.html"},
        name="password_reset_done"),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', password_reset_confirm,
        {'template_name': 'posts/users//password_reset_confirm.html'},
        name='password_reset_confirm'
        ),
    url(r'^reset/done', password_reset_complete, {'template_name': 'posts/users/password_reset_complete.html'},
        name='password_reset_complete'),
]
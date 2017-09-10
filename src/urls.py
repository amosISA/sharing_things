"""sharing_things URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import logout_then_login, password_reset, password_reset_done, password_reset_confirm, password_reset_complete

from . import views
from profiles.views import ProfileFollowToggle, activate_user_view

from django.contrib.auth.views import LoginView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^profile/', include('profiles.urls', namespace='profiles')),
    url(r'^posts/', include('posts.urls', namespace='posts')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^$', views.src_index),

    #url(r'^accounts/login/', login, {'template_name': 'login.html'}, name='login'),
    url(r'^accounts/login/', views.custom_login, {'template_name':'login.html'}, name='login'),
    url(r'^register/$', views.RegisterView.as_view(), name="register"),
    url(r'^activate/(?P<code>[a-z0-9].*)/$', activate_user_view, name='activate'),
    url(r'^logout/', logout_then_login, name='logout'),

    url(r'^profile-follow/$', ProfileFollowToggle.as_view(), name='follow'),

    url(r'^reset/password_reset', password_reset, {"template_name": "password_reset_form.html",
        "email_template_name": "password_reset_email.html"}, name="password_reset"),
    url(r'^password_reset_done', password_reset_done, {"template_name":"password_reset_done.html"},
        name="password_reset_done"),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', password_reset_confirm,
        {'template_name': 'password_reset_confirm.html'},
        name='password_reset_confirm'
        ),
    url(r'^reset/done', password_reset_complete, {'template_name': 'password_reset_complete.html'},
        name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
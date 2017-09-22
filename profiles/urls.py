from .views import ProfileDetailView, upload_avatar, UserLikesDetailView
from django.conf.urls import url

urlpatterns = [
    url(r'^(?P<username>[\w-]+)/$', ProfileDetailView.as_view(), name='user_profile'),
    url(r'^upload/avatar/$', upload_avatar, name='upload_avatar'),
    url(r'^likes/(?P<username>[\w-]+)/$', UserLikesDetailView.as_view(), name='user_likes'),
]
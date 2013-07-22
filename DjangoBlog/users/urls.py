from django.conf.urls import patterns, url

from users.views import SignUp


urlpatterns = patterns('users.views',
    # url(r'^login/$', 'login'),
    # url(r'^logout/$', 'logout'),
    url(r'^signup/$', SignUp.as_view(), name='users_SignUp'),
)

from django.conf.urls import patterns, url

from users.views import SignUp, Login, Logout


urlpatterns = patterns('users.views',
    url(r'^login/$', Login.as_view(), name='users_Login'),
    url(r'^logout/$', Logout.as_view(), name='users_Logout'),
    url(r'^signup/$', SignUp.as_view(), name='users_SignUp'),
)

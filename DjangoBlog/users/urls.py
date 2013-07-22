from django.conf.urls import patterns, url

from users.views import EditUser, Login, Logout, SignUp


urlpatterns = patterns('users.views',
    url(r'^login/$', Login.as_view(), name='users_Login'),
    url(r'^logout/$', Logout.as_view(), name='users_Logout'),
    url(r'^signup/$', SignUp.as_view(), name='users_SignUp'),
    url(r'^edit/(?P<id>[0-9]+)$', EditUser.as_view(), name='users_EditUser'),
)

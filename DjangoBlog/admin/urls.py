from django.conf.urls import patterns, url

from admin.views import AdminHome, AdminPostList, AdminUserList

urlpatterns = patterns('users.views',
    url(r'^$', AdminHome.as_view(), name='admin_AdminHome'),
    url(r'^posts/$', AdminPostList.as_view(), name='admin_AdminPostList'),
    url(r'^users/$', AdminUserList.as_view(), name='admin_AdminUserList'),
)

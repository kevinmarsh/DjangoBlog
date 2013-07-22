from django.conf.urls import patterns, url

from blog.views import HomePage, EditPost, NewPost, SinglePost

urlpatterns = patterns('blog.views',
    url(r'^$', HomePage.as_view(), name='blog_HomePage'),
    url(r'^newpost/$', NewPost.as_view(), name='blog_NewPost'),
    url(r'^post/(?P<slug>[\w-]+)$', SinglePost.as_view(), name='blog_SinglePost'),
    url(r'^edit/(?P<id>[\w-]+)$', EditPost.as_view(), name='blog_EditPost'),
)

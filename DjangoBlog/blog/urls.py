from django.conf.urls import patterns, url

from blog.views import HomePage, NewPost, SinglePost

# urlpatterns = patterns('views',
urlpatterns = patterns('blog.views',
# urlpatterns = patterns('DjangoBlog.blog.views',
    url(r'^$', HomePage.as_view(), name='blog_HomePage'),
    url(r'^newpost/$', NewPost.as_view(), name='blog_NewPost'),
    url(r'^post/(?P<slug>[\w-]+)$', SinglePost.as_view(), name='blog_SinglePost'),
)

# urlpatterns += patterns('users.views',
#     url(r'^login/$', 'login'),
#     url(r'^logout/$', 'logout'),
#     url(r'^signup/$', 'signUp'),
# )

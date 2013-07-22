from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin

# from blog.views import HomePage

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='base.html')),
    # url(r'^$', HomePage.as_view(), name='home'),

    # Examples:
    # url(r'^$', 'DjangoBlog.views.home', name='home'),
    url(r'^blog/', include('blog.urls')),
    # url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^users/', include('users.urls')),
    # url(r'^users/', include('users.urls', namespace='users')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

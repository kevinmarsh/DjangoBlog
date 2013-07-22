from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

# from blog.views import HomePage

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='base.html')),
    # url(r'^$', HomePage.as_view(), name='home'),

    url(r'^blog/', include('blog.urls')),
    url(r'^users/', include('users.urls')),

    url(r'^admin/', include(admin.site.urls)),
)



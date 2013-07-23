from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic import TemplateView

from blog.models import BlogPost
from mixins import LoginRequiredMixin


class AdminHome(LoginRequiredMixin, TemplateView):
    template_name = 'admin_home.html'


class AdminPostList(LoginRequiredMixin, View):
    def get(self, request):
        blogPosts = BlogPost.objects.all()
        return render(request, 'admin_all_posts.html', {'blogPosts': blogPosts})


class AdminUserList(LoginRequiredMixin, View):
    def get(self, request):
        users = User.objects.all()
        return render(request, 'admin_all_users.html', {'users': users})

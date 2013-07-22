from django.shortcuts import render
from django.views.generic.base import View

from blog.models import BlogPost


class AdminHome(View):
    pass


class AdminPostList(View):
    def get(self, request):
        blogPosts = BlogPost.objects.all()
        return render(request, 'admin_all_posts.html', {'blogPosts': blogPosts})


class AdminUserList(View):
    pass

import string
import re

from django.contrib import messages
# from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
# from django.utils.decorators import method_decorator
from django.views.generic.base import View

from blog.models import BlogPost
from mixins import LoginRequiredMixin


def titleToUrl(title):
    """Converts a title (punctuated text string) to a dash seperated url w/o stop words"""
    PUNC = set(string.punctuation)                                              # Punctuation chars
    STOPWORDS = 'a,able,about,across,after,all,almost,also,am,among,an,and,any,are,as,at,be,because,been,but,by,can,cannot,could,dear,did,do,does,either,else,ever,every,for,from,get,got,had,has,have,he,her,hers,him,his,how,however,i,if,in,into,is,it,its,just,least,let,like,likely,may,me,might,most,must,my,neither,no,nor,not,of,off,often,on,only,or,other,our,own,rather,said,say,says,she,should,since,so,some,than,that,the,their,them,then,there,these,they,this,tis,to,too,twas,us,wants,was,we,were,what,when,where,which,while,who,whom,why,will,with,would,yet,you,your'.split(',')
    title = re.sub('<[^<]+?>', '', title)                                       # Strip out any html in the title
    title = ''.join(let for let in title if let not in PUNC).lower().split()    # List of words w/o punc and lowercased
    return '-'.join([word for word in title if word not in STOPWORDS])          # Checks word isn't a stop word then joins with a dash


class HomePage(View):
    def get(self, request):
        blogPosts = BlogPost.objects.filter(published=True).order_by('-created')
        return render(request, 'blog_home.html', {'blogPosts': blogPosts})


class SinglePost(View):
    def get(self, request, slug):
        try:
            blogPost = BlogPost.objects.get(slug=slug)
        except BlogPost.DoesNotExist:
            messages.add_message(request, messages.INFO, 'That blog post does not exist.')
            return HttpResponseRedirect(reverse('blog_HomePage'))
        return render(request, 'blog_post.html', {'post': blogPost})


class NewPost(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'blog_create.html', {})

    def post(self, request):
        subject = request.POST['subject']
        content = request.POST['content']
        slug = titleToUrl(subject)
        published = request.POST['published'] == 'published'

        if not subject:
            messages.add_message(request, messages.INFO, 'Please add a subject.')
        if not content:
            messages.add_message(request, messages.INFO, 'Please add some content.')
        if not BlogPost.objects.filter(slug=slug).count() == 0:
            messages.add_message(request, messages.INFO, 'Please rename, you\'ve used that title before.')
        if messages.get_messages(request):
            params = {'subject': subject,
                      'content': content,
                      'published': published}
            return render(request, 'blog_create.html', params)
        else:
            post = BlogPost(title=subject,
                            body=content,
                            slug=slug,
                            published=published)
            post.save()
            messages.add_message(request, messages.SUCCESS, 'Blog post created.')
            return HttpResponseRedirect(reverse('blog_SinglePost', args=(slug,)))


class EditPost(LoginRequiredMixin, View):
    def get(self, request, id):
        try:
            blogPost = BlogPost.objects.get(id=id)
        except BlogPost.DoesNotExist:
            messages.add_message(request, messages.INFO, 'That blog post does not exist.')
            return HttpResponseRedirect(reverse('blog_HomePage'))
        return render(request, 'blog_edit.html', {'post': blogPost})

    def post(self, request, id):
        try:
            blogPost = BlogPost.objects.get(id=id)
        except BlogPost.DoesNotExist:
            messages.add_message(request, messages.INFO, 'That blog post does not exist.')
            return HttpResponseRedirect(reverse('blog_HomePage'))

        title = request.POST['title']
        body = request.POST['body']
        slug = request.POST['slug']
        published = request.POST['published'] == 'published'
        if not title:
            messages.add_message(request, messages.INFO, 'Please add a title.')
        if not body:
            messages.add_message(request, messages.INFO, 'Please add some content.')
        if title and not BlogPost.objects.filter(slug=slug).exclude(id=id).count() == 0:
            messages.add_message(request, messages.INFO, 'Please rename, you\'ve used that title before.')
        if messages.get_messages(request):
            blogPost = {'title': title,
                        'body': body,
                        'slug': slug,
                        'published': published}
            return render(request, 'blog_edit.html', {'post': blogPost})

        blogPost.title = title
        blogPost.body = body
        blogPost.slug = slug
        blogPost.published = published
        blogPost.save()
        messages.add_message(request, messages.SUCCESS, 'Blog post edited.')
        return HttpResponseRedirect(reverse('blog_SinglePost', args=(slug,)))

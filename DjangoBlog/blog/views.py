import string
import re

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View

from blog.models import BlogPost


def titleToUrl(title):
    """Converts a title (punctuated text string) to a dash seperated url w/o stop words"""
    PUNC = set(string.punctuation)                                              # Punctuation chars
    STOPWORDS = 'a,able,about,across,after,all,almost,also,am,among,an,and,any,are,as,at,be,because,been,but,by,can,cannot,could,dear,did,do,does,either,else,ever,every,for,from,get,got,had,has,have,he,her,hers,him,his,how,however,i,if,in,into,is,it,its,just,least,let,like,likely,may,me,might,most,must,my,neither,no,nor,not,of,off,often,on,only,or,other,our,own,rather,said,say,says,she,should,since,so,some,than,that,the,their,them,then,there,these,they,this,tis,to,too,twas,us,wants,was,we,were,what,when,where,which,while,who,whom,why,will,with,would,yet,you,your'.split(',')
    title = re.sub('<[^<]+?>', '', title)                                       # Strip out any html in the title
    title = ''.join(let for let in title if let not in PUNC).lower().split()    # List of words w/o punc and lowercased
    return '-'.join([word for word in title if word not in STOPWORDS])          # Checks word isn't a stop word then joins with a dash


class HomePage(View):
    def get(self, request):
        blogPosts = BlogPost.objects.all().order_by('-created')
        return render(request, 'blog_home.html', {'blogPosts': blogPosts})


class SinglePost(View):
    def get(self, request, slug):
        blogPost = BlogPost.objects.get(slug=slug)
        return render(request, 'blog_post.html', {'post': blogPost})


class NewPost(View):
    def get(self, request):
        return render(request, 'blog_create.html', {})

    def post(self, request):
        subject = request.POST['subject']
        content = request.POST['content']
        slug = titleToUrl(subject)

        if not subject:
            messages.add_message(request, messages.INFO, 'Please add a subject.')
        if not content:
            messages.add_message(request, messages.INFO, 'Please add some content.')
        if not BlogPost.objects.filter(slug=slug).count() == 0:
            messages.add_message(request, messages.INFO, 'Please rename, you\'ve used that title before.')
        if messages.get_messages(request):
            params = {'subject': subject,
                      'content': content}
            return render(request, 'blog_create.html', params)
        else:
            post = BlogPost(title=subject,
                            body=content,
                            slug=slug)
            post.save()
            messages.add_message(request, messages.SUCCESS, 'Blog post created.')
            return HttpResponseRedirect(reverse('blog_SinglePost', args=(slug,)))

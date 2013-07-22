from django.db import models


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BlogPost(TimeStampedModel):
    title = models.CharField(max_length=30)
    body = models.TextField()
    slug = models.SlugField(null=False, unique=True)
    published = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s' % self.title

    @models.permalink
    def get_absolute_url(self):
        return ('blog_SinglePost', None, {'slug': self.slug})

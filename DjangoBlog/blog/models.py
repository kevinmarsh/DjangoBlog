from django.contrib.auth.models import User
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

    # TODO: add these as a kind of history on the post page
    # created_by = models.ForeignKey(User)
    # modified_by = models.ForeignKey(User)

    def __unicode__(self):
        return '%s' % self.title

    class Meta:
        ordering = ["-published"]

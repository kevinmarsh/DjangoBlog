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
    published = models.BooleanField(default=True)

    # TODO: creator of blog post
    # created_by = models.ForeignKey(User)

    def __unicode__(self):
        return '%s' % self.title

    class Meta:
        ordering = ["-published"]

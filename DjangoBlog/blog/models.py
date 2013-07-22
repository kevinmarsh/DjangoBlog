from django.db import models


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BlogPost(TimeStampedModel):
    title = models.CharField(max_length=30)
    body = models.TextField()
    # tags = models.CharField(repeated=True)
    url = models.SlugField(unique=True)

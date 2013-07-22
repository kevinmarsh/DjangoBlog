from django.db import models

from blog.models import TimeStampedModel

class User(TimeStampedModel):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    admin = models.BooleanField(default=False)

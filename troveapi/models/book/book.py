from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    current = models.BooleanField()
    tags = models.ManyToManyField(
        "Tag", through="TaggedBook", related_name="bookTags")

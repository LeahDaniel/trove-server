from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    author = models.ForeignKey("Author", on_delete=models.CASCADE, related_name="book_author")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    current = models.BooleanField()
    last_modified = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(
        "Tag", through="TaggedBook", related_name="book_tags")

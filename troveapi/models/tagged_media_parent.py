from django.db import models
from .tag import Tag


class TaggedMedia(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

from django.contrib.auth.models import User
from django.db import models
from .game.tagged_game import TaggedGame
from .show.tagged_show import TaggedShow
from .book.tagged_book import TaggedBook


class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.CharField(max_length=40)

    # look into uniqueConstraints?




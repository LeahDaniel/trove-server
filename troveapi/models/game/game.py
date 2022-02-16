from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    multiplayer_capable = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    current = models.BooleanField()
    last_modified = models.DateTimeField(auto_now=True)
    platforms = models.ManyToManyField(
        "Platform", through="GamePlatform", related_name="platforms")
    tags = models.ManyToManyField(
        "Tag", through="TaggedGame", related_name="game_tags")


from django.db import models


class TaggedGame(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE)

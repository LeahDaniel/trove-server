from django.db import models


class GamePlatform(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    platform = models.ForeignKey("Platform", on_delete=models.CASCADE)
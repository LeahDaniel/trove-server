from django.db import models
from django.contrib.auth.models import User


class GameRecommendation(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gameSender')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gameRecipient')
    message = models.TextField()
    read = models.BooleanField(default=False)

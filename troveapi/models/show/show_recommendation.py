from django.db import models
from django.contrib.auth.models import User


class ShowRecommendation(models.Model):
    show = models.ForeignKey("Show", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='showSender')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='showRecipient')
    message = models.TextField()
    read = models.BooleanField(default=False)

    
    
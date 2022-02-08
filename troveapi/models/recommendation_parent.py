from django.contrib.auth.models import User
from django.db import models


class Recommendation(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')
    message = models.TextField()
    read = models.BooleanField(default=False)

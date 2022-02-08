from django.db import models
from django.contrib.auth.models import User


class BookRecommendation(models.Model):
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookSender')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookRecipient')
    message = models.TextField()
    read = models.BooleanField(default=False)

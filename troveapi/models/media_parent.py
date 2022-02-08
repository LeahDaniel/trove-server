from django.contrib.auth.models import User
from django.db import models


class Media(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    current = models.BooleanField()

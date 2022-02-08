from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.CharField(max_length=40)

    # look into uniqueConstraints?

from django.db import models


class StreamingService(models.Model):
    service = models.CharField(max_length=15)
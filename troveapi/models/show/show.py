from django.db import models
from django.contrib.auth.models import User

class Show(models.Model):
    streaming_service= models.ForeignKey("StreamingService", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    current = models.BooleanField()
    last_modified = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(
        "Tag", through="TaggedShow", related_name="showTags")
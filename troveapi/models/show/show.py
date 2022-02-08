from tkinter import CASCADE
from django.db import models
from ..media_parent import Media

class Show(Media):
    streaming_service= models.ForeignKey("StreamingService", on_delete=models.CASCADE)
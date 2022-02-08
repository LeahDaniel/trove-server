from django.db import models
from ..media_parent import Media

class Book(Media):
    author= models.ForeignKey("Author", on_delete=models.CASCADE)
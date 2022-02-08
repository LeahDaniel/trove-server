from django.db import models


class TaggedBook(models.Model):
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE)

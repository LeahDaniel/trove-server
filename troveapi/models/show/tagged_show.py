from django.db import models


class TaggedShow(models.Model):
    show = models.ForeignKey("Show", on_delete=models.CASCADE)
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE)

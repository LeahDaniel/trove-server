from django.db import models
from ..tagged_media_parent import TaggedMedia


class TaggedShow(TaggedMedia):
    show = models.ForeignKey("Show", on_delete=models.CASCADE)

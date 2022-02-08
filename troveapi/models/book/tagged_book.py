from django.db import models
from ..tagged_media_parent import TaggedMedia


class TaggedBook(TaggedMedia):
    book = models.ForeignKey("Book", on_delete=models.CASCADE)

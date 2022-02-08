from django.db import models
from ..tagged_media_parent import TaggedMedia


class TaggedGame(TaggedMedia):
    game = models.ForeignKey("Game", on_delete=models.CASCADE)

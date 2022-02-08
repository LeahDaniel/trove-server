from django.db import models
from ..media_parent import Media


class Game(Media):
    multiplayer_capable= models.BooleanField()
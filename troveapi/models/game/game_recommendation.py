from django.db import models
from ..recommendation_parent import Recommendation


class GameRecommendation(Recommendation):
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
from django.db import models
from ..recommendation_parent import Recommendation


class ShowRecommendation(Recommendation):
    show = models.ForeignKey("Show", on_delete=models.CASCADE)
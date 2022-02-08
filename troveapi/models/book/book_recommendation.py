from django.db import models
from ..recommendation_parent import Recommendation


class BookRecommendation(Recommendation):
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
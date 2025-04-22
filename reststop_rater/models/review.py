# /backend/reststop_rater/models/review.py

from django.db import models
from django.contrib.auth.models import User
from .bathroom import Bathroom
from ..services.bathroom import update_bathroom_rating

class Review(models.Model):
    bathroom = models.ForeignKey(Bathroom, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
        models.UniqueConstraint(fields=['user', 'bathroom'], name='unique_user_review')
    ]

    def __str__(self):
        return f'{self.user.username} review on {self.bathroom.name}'
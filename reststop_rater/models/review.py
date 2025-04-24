# /backend/reststop_rater/models/review.py

from django.db import models
from django.contrib.auth.models import User
from .bathroom import Bathroom

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

    def update_bathroom_rating_after_review_change(self):
        self.bathroom.update_bathroom_rating()

    def handle_review_creation_or_deletion(self, action='create'):
        if action == 'create':
            self.update_bathroom_rating_after_review_change()
        elif action == 'delete':
            self.update_bathroom_rating_after_review_change()

    @classmethod
    def get_reviews(cls, updated_since=None):
        qs = Review.objects.select_related('user', 'bathroom')
        if updated_since:
            qs = qs.filter(updated_at__gte=updated_since)
        return qs
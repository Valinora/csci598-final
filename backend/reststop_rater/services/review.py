# /backend/reststop_rater/services/review.py

from ..models.review import Review

def get_reviews(updated_since=None):
    qs = Review.objects.select_related('user', 'bathroom')
    if updated_since:
        qs = qs.filter(updated_at__gte=updated_since)
    return qs

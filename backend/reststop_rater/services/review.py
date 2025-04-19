# /backend/reststop_rater/services/review.py

from ..models.review import Review
from ..models.bathroom import Bathroom

def update_bathroom_rating_after_review_change(review):
    bathroom = review.bathroom
    reviews = bathroom.reviews.all()
    if reviews.exists():
        avg_rating = sum([r.rating for r in reviews]) / reviews.count()
        bathroom.rating = round(avg_rating, 2)
    else:
        bathroom.rating = 0.0
    bathroom.save(update_fields=["rating"])

def handle_review_creation_or_deletion(review, action='create'):
    if action == 'create':
        update_bathroom_rating_after_review_change(review)
    elif action == 'delete':
        update_bathroom_rating_after_review_change(review)

def get_reviews(updated_since=None):
    qs = Review.objects.select_related('user', 'bathroom')
    if updated_since:
        qs = qs.filter(updated_at__gte=updated_since)
    return qs
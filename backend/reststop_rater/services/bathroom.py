# /backend/reststop_rater/services/bathroom.py

from ..models.bathroom import Bathroom

def get_bathrooms(updated_since=None):
    qs = Bathroom.objects.prefetch_related('reviews__user')
    if updated_since:
        qs = qs.filter(updated_at__gte=updated_since)
    return qs

def get_nearby_bathrooms(lat, lng, radius_km=5.0):
    bathrooms = Bathroom.objects.all()
    return [
        b for b in bathrooms
        if b.distance_to(lat, lng) <= radius_km
    ]

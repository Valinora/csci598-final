# /backend/reststop_rater/services/bathroom.py
from math import radians, sin, cos, sqrt, atan2
from ..models.bathroom import Bathroom

def update_bathroom_rating(bathroom):
    reviews = bathroom.reviews.all()
    if reviews.exists():
        avg_rating = sum([r.rating for r in reviews]) / reviews.count()
        bathroom.rating = round(avg_rating, 2)
    else:
        bathroom.rating = 0.0
    bathroom.save(update_fields=["rating"])

class BathroomService:
    
    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        R = 6371
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

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

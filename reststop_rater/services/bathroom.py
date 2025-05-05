from math import radians, sin, cos, sqrt, atan2
from ..models.bathroom import Bathroom

def update_bathroom_rating(bathroom):
    reviews = bathroom.reviews.all()
    total_rating = 0
    count = 0

    if reviews.exists():
        total_rating += sum(r.rating for r in reviews)
        count += reviews.count()

    for star, qty in bathroom.quick_rate.items():
        total_rating += int(star) * qty
        count += qty

    bathroom.rating = round(total_rating / count, 2) if count > 0 else 0.0
    bathroom.save(update_fields=["rating"])


class BathroomService:
    
    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        lat1 = float(lat1)
        lon1 = float(lon1)
        lat2 = float(lat2)
        lon2 = float(lon2)
        R = 3958.8
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

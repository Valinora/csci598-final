# /backend/reststop_rater/models/bathroom.py

from math import radians, sin, cos, sqrt, atan2
from django.db import models


class Bathroom(models.Model):
    name = models.CharField(max_length=100)
    rating = models.FloatField(default=0.0)
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        R = 6371
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = (
            sin(dlat / 2) ** 2
            + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
        )
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

    def distance_to(self, other):
        return Bathroom.calculate_distance(
            self.latitude, self.longitude, other.lat2, other.lon2
        )

    @classmethod
    def get_bathrooms(cls, updated_since=None):
        qs = Bathroom.objects.prefetch_related("reviews__user")
        if updated_since:
            qs = qs.filter(updated_at__gte=updated_since)
        return qs

    @classmethod
    def get_nearby_bathrooms(cls, lat, lng, radius_km=5.0):
        bathrooms = Bathroom.objects.all()
        return [b for b in bathrooms if b.distance_to(lat, lng) <= radius_km]

    def update_bathroom_rating(self): # This should probably be a trigger in the DB, not sure how to do it.
        reviews = self.reviews.all()
        if reviews.exists():
            avg_rating = sum([r.rating for r in reviews]) / reviews.count()
            self.rating = round(avg_rating, 2)
        else:
            self.rating = 0.0
        self.save(update_fields=["rating"])

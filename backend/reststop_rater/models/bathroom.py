# /backend/reststop_rater/models/bathroom.py

from django.db import models
from math import radians, sin, cos, sqrt, atan2

class Bathroom(models.Model):
    name = models.CharField(max_length=100)
    rating = models.FloatField(default=0.0)
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
    
    def distance_to(self, lat2, lon2):
        R = 6371  # Earth radius in km
        lat1, lon1 = self.latitude, self.longitude
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c
    
    def update_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            avg_rating = sum([r.rating for r in reviews]) / reviews.count()
            self.rating = round(avg_rating, 2)
        else:
            self.rating = 0.0
        self.save(update_fields=["rating"])

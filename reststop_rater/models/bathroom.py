# /backend/reststop_rater/models/bathroom.py

from django.db import models

class Bathroom(models.Model):
    name = models.CharField(max_length=100)
    rating = models.FloatField(default=0.0)
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gmaps_id = models.CharField(max_length=50, null=True, unique=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
    
    def distance_to(self, lat2, lon2):
        from ..services.bathroom import BathroomService
        return BathroomService.calculate_distance(self.latitude, self.longitude, lat2, lon2)

    @classmethod
    def create_bathroom(cls, name, address, lat, long):
        ret = cls(name=name, address=address, latitude=lat, longitude=long)
        ret.save()
        return ret

from django.db import models
from django.contrib.auth.models import User

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

    def __str__(self ):
        return self.name
    
class Review(models.Model):
    bathroom = models.ForeignKey(Bathroom, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} review on {self.bathroom.name}'
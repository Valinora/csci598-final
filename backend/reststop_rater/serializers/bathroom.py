# /backend/reststop_rater/serializers/bathroom.py

from rest_framework import serializers
from .review import ReviewSerializer
from ..models.bathroom import Bathroom

class BathroomSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Bathroom
        fields = ['id', 'name', 'rating', 'address', 'latitude', 'longitude', 'created_at', 'reviews']
        read_only_fields = ['id', 'created_at', 'reviews']
        extra_kwargs = {
            'rating': {'default': 0.0} 
        }

    def validate_rating(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError("Rating must be between 0 and 5.")
        return value

from rest_framework import serializers
from .review import ReviewSerializer
from ..models.bathroom import Bathroom

class BathroomSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, required=False)

    class Meta:
        model = Bathroom
        fields = ['id', 'name', 'rating', 'address', 'latitude', 'longitude', 'created_at', 'reviews']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            # Rating defaults to 0 if not provided
            'rating': {'default': 0.0} 
        }

    def validate_rating(self, value):
        # Ensure the rating is within a valid range
        if value < 0 or value > 5:
            raise serializers.ValidationError("Rating must be between 0 and 5.")
        return value

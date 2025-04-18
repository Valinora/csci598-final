from rest_framework import serializers
from .models import Bathroom, Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

class BathroomSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Bathroom
        fields = ['id', 'name', 'rating', 'address', 'latitude', 'longitude', 'created_at', 'reviews']

    def __init__(self, *args, **kwargs):
        exclude_reviews = kwargs.pop('exclude_reviews', False)
        super().__init__(*args, **kwargs)

        if exclude_reviews:
            self.fields.pop('reviews')
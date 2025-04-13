from rest_framework import serializers
from .models import Bathroom, Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at']

class BathroomSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Bathroom
        fields = ['id', 'name', 'rating', 'address', 'latitude', 'longitude', 'created_at', 'reviews']
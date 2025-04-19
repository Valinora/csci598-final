# src/serializers/review.py
from rest_framework import serializers
from ..models.review import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'bathroom', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    def create(self, validated_data):
        # Automatically set the user
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

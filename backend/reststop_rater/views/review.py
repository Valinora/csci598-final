# /backend/reststop_rater/views/review.py

from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from ..models.review import Review
from ..serializers.review import ReviewSerializer
from ..models.bathroom import Bathroom

class BathroomReviewListView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(bathroom_id=self.kwargs["pk"]).select_related("user")

    def perform_create(self, serializer):
        # Automatically assign the logged-in user to the review
        bathroom = get_object_or_404(Bathroom, pk=self.kwargs["pk"])
        serializer.save(user=self.request.user, bathroom=bathroom)

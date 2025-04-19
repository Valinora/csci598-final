from rest_framework import generics, permissions

from ..models.bathroom import Bathroom
from ..serializers.bathroom import BathroomSerializer

class BathroomListCreateView(generics.ListCreateAPIView):
    queryset = Bathroom.objects.prefetch_related('reviews__user')
    serializer_class = BathroomSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BathroomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bathroom.objects.prefetch_related('reviews__user')
    serializer_class = BathroomSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

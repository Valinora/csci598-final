# /backend/reststop_rater/views/bathroom.py

from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.bathroom import Bathroom
from ..serializers.bathroom import BathroomSerializer
from ..services.bathroom import get_nearby_bathrooms
from ..viewmodels.bathroom import BathroomViewModel


class BathroomListCreateView(generics.ListCreateAPIView):
    queryset = Bathroom.objects.prefetch_related('reviews__user')
    serializer_class = BathroomSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BathroomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bathroom.objects.prefetch_related('reviews__user')
    serializer_class = BathroomSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class NearbyBathroomsView(APIView):
    def get(self, request):
        lat_param = request.query_params.get("latitude")
        lng_param = request.query_params.get("longitude")

        if lat_param is None or lng_param is None:
            return Response(
                {"error": "Missing latitude or longitude in query parameters."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            lat = float(lat_param)
            lng = float(lng_param)
            radius_km = float(request.query_params.get("radius", 5))
        except ValueError:
            return Response(
                {"error": "Invalid coordinates or radius."},
                status=status.HTTP_400_BAD_REQUEST
            )

        bathrooms = get_nearby_bathrooms(lat, lng, radius_km)
        response = [
            BathroomViewModel.from_model(b, b.distance_to(lat, lng)).__dict__
            for b in bathrooms
        ]
        return Response(response)
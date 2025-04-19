# /backend/reststop_rater/views/sync.py

from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.dateparse import parse_datetime
from ..services.review import get_reviews
from ..services.bathroom import get_bathrooms
from ..serializers.review import ReviewSerializer
from ..serializers.bathroom import BathroomSerializer

class SyncView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        since = parse_datetime(request.query_params.get('since')) if 'since' in request.query_params else None
        bathrooms = get_bathrooms(since)
        reviews = get_reviews(since)

        return Response({
            'bathrooms': BathroomSerializer(bathrooms, many=True).data,
            'reviews': ReviewSerializer(reviews, many=True).data,
        })

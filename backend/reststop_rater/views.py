# Standard library imports
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime

# Django REST Framework imports
from rest_framework import status, permissions, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

# Local app imports
from .models import Bathroom, Review
from .serializers import (
    BathroomSerializer,
    ReviewSerializer,
    BathroomWithReviewsSerializer
)

# ─── API Root ────────────────────────────────────────────────────────────────────
# View at /api/ that shows all of the endpoints accessible from this root
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'signup': {
            'url': reverse('signup', request=request, format=format),
            'methods': ['POST'],
            'description': 'Create a new user account',
        },
        'login': {
            'url': reverse('token_obtain_pair', request=request, format=format),
            'methods': ['POST'],
            'description': 'Obtain JWT token pair',
        },
        'token_refresh': {
            'url': reverse('token_refresh', request=request, format=format),
            'methods': ['POST'],
            'description': 'Refresh JWT access token',
        },
        'bathrooms': {
            'url': reverse('bathroom-list-create', request=request, format=format),
            'methods': ['GET', 'POST'],
            'description': 'List all bathrooms or create a new one',
        },
        'bathroom_detail': {
            'example_url': reverse('bathroom-detail', kwargs={'pk': 1}, request=request, format=format),
            'methods': ['GET', 'PUT', 'DELETE'],
            'description': 'Retrieve, update, or delete a specific bathroom',
        },
        'all_reviews': {
            'url': reverse('all-reviews', request=request, format=format),
            'methods': ['GET'],
            'description': 'List all reviews across all bathrooms (read-only)',
        },
        'reviews_for_bathroom': {
            'example_url': reverse('review-list-create', kwargs={'bathroom_id': 1}, request=request, format=format),
            'methods': ['GET', 'POST'],
            'description': 'List or create reviews for a specific bathroom, with bathroom_id number',
        },
        'sync': {
            'url': reverse('sync-endpoint', request=request, format=format),
            'methods': ['GET'],
            'description': 'Fetch all bathrooms and associated reviews in one call',
        },
    })

# ─── User Signup ────────────────────────────────────────────────────────────────
class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password)
        return Response({"message": "User created"}, status=status.HTTP_201_CREATED)

# ─── Bathroom Views ─────────────────────────────────────────────────────────────
class BathroomListCreateView(generics.ListCreateAPIView):
    queryset = Bathroom.objects.all().order_by('-created_at')
    serializer_class = BathroomSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BathroomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bathroom.objects.all()
    serializer_class = BathroomSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# ─── Review Views ───────────────────────────────────────────────────────────────
# List or create reviews for a specific bathroom
class BathroomReviewListView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        bathroom_id = self.kwargs['bathroom_id']
        return Review.objects.filter(bathroom__id=bathroom_id)

    def perform_create(self, serializer):
        bathroom = Bathroom.objects.get(pk=self.kwargs['bathroom_id'])
        serializer.save(user=self.request.user, bathroom=bathroom)

# Not currently in use: general review list endpoint (not tied to bathrooms)
class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Read-only endpoint for all reviews
class AllReviewsView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


# ─── Sync Endpoint ──────────────────────────────────────────────────────────────
# Combines bathrooms and associated reviews into one response (optionally filtered by updated_at timestamp)
class SyncView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        since = request.query_params.get('since')
        if since:
            try:
                since_dt = parse_datetime(since)
            except ValueError:
                return Response({'error': 'Invalid datetime format'}, status=400)
            bathrooms = Bathroom.objects.filter(updated_at__gte=since_dt)
            reviews = Review.objects.filter(updated_at__gte=since_dt)
        else:
            bathrooms = Bathroom.objects.all()
            reviews = Review.objects.all()

        return Response({
            'bathrooms': BathroomWithReviewsSerializer(bathrooms, many=True).data,
            'reviews': ReviewSerializer(reviews, many=True).data,
        })
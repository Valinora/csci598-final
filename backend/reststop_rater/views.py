# Standard library imports
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime
from django.shortcuts import get_object_or_404

# Django REST Framework imports
from rest_framework import status, permissions, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

# Local app imports
from .models import Bathroom, Review
from .serializers import BathroomSerializer, ReviewSerializer

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
            'example_url': reverse('review-list-create', kwargs={'pk': 1}, request=request, format=format),
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

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email", "")  # Optional email field

        # Check for missing fields
        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create the user
            user = User.objects.create_user(username=username, password=password, email=email)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)

# ─── Bathroom Views ─────────────────────────────────────────────────────────────
# Helper class
class BaseBathroomView:
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = BathroomSerializer
    queryset = Bathroom.objects.all()

class BathroomListCreateView(BaseBathroomView, generics.ListCreateAPIView):
    pass

class BathroomDetailView(BaseBathroomView, generics.RetrieveUpdateDestroyAPIView):
    pass

# ─── Review Views ───────────────────────────────────────────────────────────────
class BaseReviewView:
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ReviewSerializer

# List or create reviews for a specific bathroom
class BathroomReviewListView(BaseReviewView, generics.ListCreateAPIView):
    def get_queryset(self):
        return Review.objects.filter(bathroom_id=self.kwargs['pk'])

    def perform_create(self, serializer):
        try:
            bathroom = get_object_or_404(Bathroom, pk=self.kwargs['pk'])
            serializer.save(user=self.request.user, bathroom=bathroom)
        except Exception as e:
            print(f"Error saving review: {e}")
            raise e

# Not currently in use: general review list endpoint (not tied to bathrooms)
class ReviewListCreateView(BaseReviewView, generics.ListCreateAPIView):
    queryset = Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Read-only endpoint for all reviews
class AllReviewsView(BaseReviewView, generics.ListAPIView):
    queryset = Review.objects.all()

# ─── Sync Endpoint ──────────────────────────────────────────────────────────────
# Combines bathrooms and associated reviews into one response (optionally filtered by updated_at timestamp)
class SyncView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        since = request.query_params.get('since')
        if since:
            since_dt = parse_datetime(since)
            if since_dt is None:
                return Response({'error': 'Invalid datetime format'}, status=400)
            bathrooms = Bathroom.objects.filter(updated_at__gte=since_dt)
            reviews = Review.objects.filter(updated_at__gte=since_dt)
        else:
            bathrooms = Bathroom.objects.all()
            reviews = Review.objects.all()

        return Response({
            'bathrooms': BathroomSerializer(bathrooms, many=True).data,
            'reviews': ReviewSerializer(reviews, many=True).data,
        })
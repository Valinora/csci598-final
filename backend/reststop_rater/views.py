from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import generics
from .models import Bathroom, Review
from .serializers import BathroomSerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Create your views here.
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
    })

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

class BathroomReviewListView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        bathroom_id = self.kwargs['bathroom_id']
        return Review.objects.filter(bathroom__id=bathroom_id)

    def perform_create(self, serializer):
        bathroom = Bathroom.objects.get(pk=self.kwargs['bathroom_id'])
        serializer.save(user=self.request.user, bathroom=bathroom)

class BathroomListCreateView(generics.ListCreateAPIView):
    queryset = Bathroom.objects.all().order_by('-created_at')
    serializer_class = BathroomSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BathroomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bathroom.objects.all()
    serializer_class = BathroomSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# Not currently in use, but allows for POST request to the general reviews list
class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AllReviewsView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
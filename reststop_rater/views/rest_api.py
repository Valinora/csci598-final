from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view

from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_datetime

from ..services.auth import create_user
from ..services.review import get_reviews
from ..services.bathroom import get_bathrooms, get_nearby_bathrooms
from ..models.review import Review
from ..models.bathroom import Bathroom
from ..serializers.review import ReviewSerializer
from ..serializers.bathroom import BathroomSerializer
from ..viewmodels.bathroom import BathroomViewModel


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "signup": {
                "url": reverse("signup", request=request, format=format),
                "methods": ["POST"],
                "description": "Create a new user account",
            },
            "login": {
                "url": reverse("token_obtain_pair", request=request, format=format),
                "methods": ["POST"],
                "description": "Obtain JWT token pair",
            },
            "token_refresh": {
                "url": reverse("token_refresh", request=request, format=format),
                "methods": ["POST"],
                "description": "Refresh JWT access token",
            },
            "bathrooms": {
                "url": reverse("bathroom-list-create", request=request, format=format),
                "methods": ["GET", "POST"],
                "description": "List all bathrooms or create a new one",
            },
            "bathroom_detail": {
                "example_url": reverse(
                    "bathroom-detail", kwargs={"pk": 1}, request=request, format=format
                ),
                "methods": ["GET", "PUT", "DELETE"],
                "description": "Retrieve, update, or delete a specific bathroom",
            },
            "reviews_for_bathroom": {
                "example_url": reverse(
                    "review-list-create",
                    kwargs={"pk": 1},
                    request=request,
                    format=format,
                ),
                "methods": ["GET", "POST"],
                "description": "List or create reviews for a specific bathroom, with bathroom_id number",
            },
            "sync": {
                "url": reverse("sync-endpoint", request=request, format=format),
                "methods": ["GET"],
                "description": "Fetch all bathrooms and associated reviews in one call",
            },
        }
    )


class SignUpView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            create_user(
                username=request.data["username"],
                password=request.data["password"],
                email=request.data.get("email", ""),
            )
            return Response(
                {"message": "User created successfully!"},
                status=status.HTTP_201_CREATED,
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BathroomListCreateView(generics.ListCreateAPIView):
    queryset = Bathroom.objects.prefetch_related("reviews__user")
    serializer_class = BathroomSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BathroomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bathroom.objects.prefetch_related("reviews__user")
    serializer_class = BathroomSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class NearbyBathroomsView(APIView):
    def get(self, request):
        lat_param = request.query_params.get("latitude")
        lng_param = request.query_params.get("longitude")

        if lat_param is None or lng_param is None:
            return Response(
                {"error": "Missing latitude or longitude in query parameters."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            lat = float(lat_param)
            lng = float(lng_param)
            radius_km = float(request.query_params.get("radius", 5))
        except ValueError:
            return Response(
                {"error": "Invalid coordinates or radius."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        bathrooms = get_nearby_bathrooms(lat, lng, radius_km)
        response = [
            BathroomViewModel.from_model(b, b.distance_to(lat, lng)).__dict__
            for b in bathrooms
        ]
        return Response(response)


class BathroomReviewListView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(bathroom_id=self.kwargs["pk"]).select_related(
            "user"
        )

    def perform_create(self, serializer):
        # Automatically assign the logged-in user to the review
        bathroom = get_object_or_404(Bathroom, pk=self.kwargs["pk"])
        serializer.save(user=self.request.user, bathroom=bathroom)


class SyncView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        since = (
            parse_datetime(request.query_params.get("since"))
            if "since" in request.query_params
            else None
        )
        bathrooms = get_bathrooms(since)
        reviews = get_reviews(since)

        return Response(
            {
                "bathrooms": BathroomSerializer(bathrooms, many=True).data,
                "reviews": ReviewSerializer(reviews, many=True).data,
            }
        )

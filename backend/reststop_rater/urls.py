# /backend/reststop_rater/urls.py

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views.auth import SignUpView
from .views.bathroom import BathroomListCreateView, BathroomDetailView,  NearbyBathroomsView
from .views.review import BathroomReviewListView
from .views.sync import SyncView
from .views.root import api_root

urlpatterns = [
    path('', api_root, name='api-root'),

    # Auth
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Bathrooms
    path('bathrooms/', BathroomListCreateView.as_view(), name='bathroom-list-create'),
    path('bathrooms/<int:pk>/', BathroomDetailView.as_view(), name='bathroom-detail'),
    path("bathrooms/nearby/", NearbyBathroomsView.as_view(), name="nearby-bathrooms"),

    # Reviews
    path('bathrooms/<int:pk>/reviews/', BathroomReviewListView.as_view(), name='review-list-create'),

    # Sync
    path('sync/', SyncView.as_view(), name='sync-endpoint'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

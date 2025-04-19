'''
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from .views import (
    SignUpView,
    BathroomListCreateView,
    BathroomDetailView,
    ReviewListCreateView,
    api_root,
    AllReviewsView,
    BathroomReviewListView,
    SyncView,
)

urlpatterns = [
    path('', api_root, name='api-root'),

    # Auth
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Bathrooms
    path('bathrooms/', BathroomListCreateView.as_view(), name='bathroom-list-create'),
    path('bathrooms/<int:pk>/', BathroomDetailView.as_view(), name='bathroom-detail'),

    # Reviews
    path('reviews/', AllReviewsView.as_view(), name='all-reviews'),
    path('bathrooms/<int:pk>/reviews/', BathroomReviewListView.as_view(), name='review-list-create'),

    # All Data
    path('sync/', SyncView.as_view(), name='sync-endpoint'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
'''
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from reststop_rater.views.auth import SignUpView
from reststop_rater.views.bathroom import BathroomListCreateView, BathroomDetailView
from reststop_rater.views.review import BathroomReviewListView
from reststop_rater.views.sync import SyncView
from reststop_rater.views.root import api_root

# from views.review import AllReviewsView  # if you have an all-reviews endpoint

urlpatterns = [
    path('', api_root, name='api-root'),

    # Auth
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Bathrooms
    path('bathrooms/', BathroomListCreateView.as_view(), name='bathroom-list-create'),
    path('bathrooms/<int:pk>/', BathroomDetailView.as_view(), name='bathroom-detail'),

    # Reviews
    # path('reviews/', AllReviewsView.as_view(), name='all-reviews'),
    path('bathrooms/<int:pk>/reviews/', BathroomReviewListView.as_view(), name='review-list-create'),

    # Sync
    path('sync/', SyncView.as_view(), name='sync-endpoint'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

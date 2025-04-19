# Django REST Framework imports
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view

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
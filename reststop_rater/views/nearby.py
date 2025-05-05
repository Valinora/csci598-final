from django.shortcuts import render
from django.views import View
import os

from ..services.bathroom import BathroomService
from ..services.gmapsapi import get_nearby_facilities
from ..models.bathroom import Bathroom

def set_location_cookie(response, lat, long):
    response.set_cookie('lat', lat, max_age=365*24*60*60)
    response.set_cookie('long', long, max_age=365*24*60*60)
    return response

def get_location_from_cookies(request):
    lat = request.COOKIES.get('lat') 
    long = request.COOKIES.get('long')
    return lat, long

class NearbyBathrooms(View):
    template = "nearby.html"

    def get(self, request):
        page_data = {"bathrooms": []}
        user_lat, user_long = None, None

        try:
            user_lat = float(request.GET.get("lat"))
            user_long = float(request.GET.get("long"))
        except (ValueError, TypeError):
            user_lat, user_long = get_location_from_cookies(request)
            if not user_lat or not user_long:
                return render(request, self.template, page_data)

        try:
            miles = float(request.GET.get("radius", 10))
            radius = int(miles * 1609.34)
        except (ValueError, TypeError):
            radius = 10000

        try:
            places_raw = get_nearby_facilities(user_lat, user_long, radius=radius)
        except Exception as e:
            print(f"Error fetching nearby places: {e}")
            return render(request, self.template, page_data)

        bathrooms = []
        for place_raw in places_raw.get("places", []):
            gmaps_id = place_raw["id"]
            address = place_raw["formattedAddress"]
            lat = float(place_raw["location"]["latitude"])
            long = float(place_raw["location"]["longitude"])
            name = place_raw["displayName"]["text"]
            distance = BathroomService.calculate_distance(user_lat, user_long, lat, long)

            photos = place_raw.get("photos", [])
            if photos:
                photo_ref = photos[0].get("name")
                photo_url = (
                    f"https://places.googleapis.com/v1/{photo_ref}/media"
                    f"?maxHeightPx=400&maxWidthPx=400&key={os.getenv('GMAPS_API_KEY')}"
                    if photo_ref else "/static/no-image.jpg"
                )
            else:
                photo_url = "/static/no-image.jpg"

            bathroom_obj, created = Bathroom.objects.get_or_create(
                gmaps_id=gmaps_id,
                defaults={
                    'name': name,
                    'address': address,
                    'latitude': lat,
                    'longitude': long,
                    'photo_url': photo_url,
                }
            )

            if not created and not bathroom_obj.photo_url and photo_url:
                bathroom_obj.photo_url = photo_url
                bathroom_obj.save()

            bathroom_obj.reviews_set = bathroom_obj.reviews.all()
            cookie_key = f"quick_rate_{bathroom_obj.id}"
            user_quick_rating = request.COOKIES.get(cookie_key)

            bathrooms.append({
                'bathroom': bathroom_obj,
                'distance': distance,
                'photo_url': photo_url,
                'user_quick_rating': user_quick_rating,
                'average_rating': bathroom_obj.rating,
                'review_count': bathroom_obj.reviews.count(),
            })

        bathrooms.sort(key=lambda b: b['distance'])
        page_data["bathrooms"] = bathrooms
        return render(request, self.template, page_data)

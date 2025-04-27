from django.shortcuts import render, redirect
from django.views import View

from ..services.bathroom import BathroomService
from ..services.gmapsapi import get_nearby_facilities
from ..models.bathroom import Bathroom

def set_location_cookie(response, lat, long):
    response.set_cookie('lat', lat, max_age=365*24*60*60)  # 1 year expiration
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
            user_lat = float(request.GET["lat"])
            user_long = float(request.GET["long"])
            
            if user_lat and user_long:
                response = render(request, self.template, page_data)
                set_location_cookie(response, user_lat, user_long)
        
        except (ValueError, KeyError):
            user_lat, user_long = get_location_from_cookies(request)
            if not user_lat or not user_long:
                return render(request, self.template, page_data)

        try:
            places_raw = get_nearby_facilities(user_lat, user_long)
        except Exception:
            return render(request, self.template, page_data)

        bathrooms = []
        for place_raw in places_raw.get("places", []):
            gmaps_id = place_raw["id"]
            address = place_raw["formattedAddress"]
            lat = float(place_raw["location"]["latitude"])
            long = float(place_raw["location"]["longitude"])
            name = place_raw["displayName"]["text"]
            distance = round(BathroomService.calculate_distance(user_lat, user_long, lat, long), ndigits=2)

            bathroom_obj, created = Bathroom.objects.get_or_create(
                gmaps_id=gmaps_id, 
                defaults={
                    'name': name,
                    'address': address,
                    'latitude': lat,
                    'longitude': long,
                }
            )
            
            bathrooms.append({
                'bathroom': bathroom_obj,
                'distance': distance,
            })

        page_data["bathrooms"] = bathrooms
        return render(request, self.template, page_data)
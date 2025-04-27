from django.shortcuts import render
from django.views import View

from ..services.bathroom import get_nearby_bathrooms, BathroomService
from ..services.gmapsapi import get_nearby_facilities
from ..models.bathroom import Bathroom



class NearbyBathrooms(View):
    template = "nearby.html"

    def get(self, request):
        page_data = {"bathrooms": []}
        try:
            lat = float(request.GET["lat"])
            long = float(request.GET["long"])
        except (ValueError, KeyError):
            return render(request, self.template, page_data)

        try:
            places_raw = get_nearby_facilities(lat, long)
        except Exception:
            return render(request, self.template, page_data)

        bathrooms = []
        for place_raw in places_raw.get("places", []):
            gmaps_id = place_raw["id"]
            address = place_raw["formattedAddress"]
            lat = float(place_raw["location"]["latitude"])
            long = float(place_raw["location"]["longitude"])
            name = place_raw["displayName"]["text"]
            distance = round(BathroomService.calculate_distance(lat, long, lat, long), ndigits=2)

            bathroom_obj, created = Bathroom.objects.get_or_create(
                gmaps_id=gmaps_id, 
                defaults={
                    'name': name,
                    'address': address,
                    'latitude': lat,
                    'longitude': long,
                    'distance': distance
                }
            )
            
            bathrooms.append(bathroom_obj)

        page_data["bathrooms"] = bathrooms

        return render(request, self.template, page_data)

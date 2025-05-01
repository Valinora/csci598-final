import requests
import json
import os

def get_nearby_facilities(lat, long, radius=50000, max_results=10):
    url = "https://places.googleapis.com/v1/places:searchNearby"
    body = {
        "included_types": ["public_bathroom", "gas_station", "rest_stop"],
        "maxResultCount": max_results,
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": lat,
                    "longitude": long,
                },
                "radius": radius,
            }
        },
    }

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": f"{os.getenv("GMAPS_API_KEY")}",
        "X-Goog-FieldMask": "places.displayName,places.location,places.formattedAddress,places.businessStatus,places.id,places.photos"
    }

    resp = requests.post(url, headers=headers, data=json.dumps(body))

    return resp.json()

def get_all_photo_urls(place_id):
    url = f"https://places.googleapis.com/v1/places/{place_id}"
    params = {
        "fields": "photos",
        "key": os.getenv("GMAPS_API_KEY")
    }

    resp = requests.get(url, params=params)
    data = resp.json()

    photo_urls = []
    for photo in data.get("photos", []):
        ref = photo.get("name")
        if ref:
            photo_urls.append(
                f"https://places.googleapis.com/v1/{ref}/media?maxWidthPx=800&key={os.getenv('GMAPS_API_KEY')}"
            )

    return photo_urls

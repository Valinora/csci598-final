import requests
import json
import os


def get_nearby_facilities(lat, long, radius=1000, max_results=10):
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
        "X-Goog-FieldMask": "places.displayName,places.location,places.formattedAddress,places.businessStatus,places.id"
    }

    resp = requests.post(url, headers=headers, data=json.dumps(body))

    return resp.json()

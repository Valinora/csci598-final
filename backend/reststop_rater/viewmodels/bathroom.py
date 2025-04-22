# /backend/reststop_rater/viewmodels/bathroom.py

from dataclasses import dataclass
from typing import List
from ..models.bathroom import Bathroom
from ..viewmodels.review import ReviewViewModel

@dataclass
class BathroomViewModel:
    id: int
    name: str
    rating: float
    address: str
    latitude: float
    longitude: float
    created_at: str
    distance_km: float  # <-- new field
    reviews: List[ReviewViewModel]

    @classmethod
    def from_model(cls, bathroom: Bathroom, distance_km: float, preloaded_reviews=None):
        reviews = preloaded_reviews or bathroom.reviews.all()
        return cls(
            id=bathroom.id,
            name=bathroom.name,
            rating=bathroom.rating,
            address=bathroom.address,
            latitude=bathroom.latitude,
            longitude=bathroom.longitude,
            created_at=bathroom.created_at.isoformat(),
            distance_km=round(distance_km, 2),
            reviews=[ReviewViewModel.from_model(r) for r in reviews]
        )

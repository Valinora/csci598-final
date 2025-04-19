from dataclasses import dataclass
from ..models.review import Review

@dataclass
class ReviewViewModel:
    id: int
    user: str
    rating: int
    comment: str
    created_at: str

    @classmethod
    def from_model(cls, review: Review):
        return cls(
            id=review.id,
            user=review.user.username,
            rating=review.rating,
            comment=review.comment,
            created_at=review.created_at.isoformat()
        )

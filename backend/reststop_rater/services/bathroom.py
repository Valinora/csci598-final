from ..models.bathroom import Bathroom

def get_bathrooms(updated_since=None):
    qs = Bathroom.objects.prefetch_related('reviews__user')
    if updated_since:
        qs = qs.filter(updated_at__gte=updated_since)
    return qs

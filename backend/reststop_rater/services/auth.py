from django.contrib.auth.models import User
from django.db import IntegrityError

def create_user(username, password, email=None):
    if not username or not password:
        raise ValueError("Username and password are required.")

    if User.objects.filter(username=username).exists():
        raise ValueError("Username already exists.")

    try:
        return User.objects.create_user(username=username, password=password, email=email)
    except IntegrityError as e:
        raise ValueError(f"Failed to create user: {str(e)}")

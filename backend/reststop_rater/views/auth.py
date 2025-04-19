from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from ..services.auth import create_user

class SignUpView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            user = create_user(
                username=request.data["username"],
                password=request.data["password"],
                email=request.data.get("email", "")
            )
            return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

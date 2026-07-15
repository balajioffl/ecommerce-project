from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer
from rest_framework.permissions import IsAuthenticated


# register

class RegisterView(APIView):
    """
    API for user registration.
    """

    permission_classes = []

    def post(self, request):
        """
        Handle POST request for user registration.
        """

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():

            user = serializer.save()

            return Response(
                {
                    "message": "User registered successfully."
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


# login

class LoginView(APIView):
    """
    API for user login.
    """

    permission_classes = []

    def post(self, request):
        """
        Handle login request.
        """

        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        user = data["user"]

        return Response(
            {
                "message": "Login successful.",
                "access": data["access"],
                "refresh": data["refresh"],
                "user": {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                },
            },
            status=status.HTTP_200_OK,
        )


# profile

class ProfileView(APIView):
    """
    API to fetch logged-in user details.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Return logged-in user details.
        """

        serializer = ProfileSerializer(request.user)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
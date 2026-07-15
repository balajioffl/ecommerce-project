from django.contrib.auth import get_user_model
from rest_framework import serializers

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

# Get the active User model.
User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer used to validate and create a new user.
    """

    # This field exists only in the request.
    # It will never be stored in the database.
    confirm_password = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = User

        fields = (
            "first_name",
            "last_name",
            "email",
            "password",
            "confirm_password",
        )

        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def validate_email(self, value):
        """
        Validate email uniqueness.
        This method is automatically called by DRF for the email field.
        """

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )

        return value

    def validate(self, attrs):
        """
        Validate the entire request.
        Used when validation depends on multiple fields.
        """

        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError(
                {
                    "confirm_password": "Passwords do not match."
                }
            )

        return attrs

    def create(self, validated_data):
        """
        Create a new user after validation succeeds.
        """

        # Remove confirm_password because
        # it is not part of the User model.
        validated_data.pop("confirm_password")

        # Use create_user() so the password
        # is hashed before saving.
        user = User.objects.create_user(
            **validated_data
        )

        return user


# login 

class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """
        Validate user credentials.
        """

        email = attrs.get("email")
        password = attrs.get("password")

        # Authenticate user
        user = authenticate(
            username=email,
            password=password,
        )

        if not user:
            raise serializers.ValidationError(
                "Invalid email or password."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "User account is disabled."
            )

        # Generate JWT Tokens
        refresh = RefreshToken.for_user(user)

        return {
            "user": user,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }


# profile

class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for logged-in user profile.
    """

    class Meta:
        model = User

        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
        )
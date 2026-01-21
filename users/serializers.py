from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=True)

    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="This email is already in use."
            )
        ]
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )

    password2 = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = ("full_name", "email", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Passwords do not match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")

        email = validated_data["email"]
        full_name = validated_data["full_name"]

        base_username = email.split("@")[0]

        user = User.objects.create_user(
            username=email,
            email=email,
            password=validated_data["password"],
        )

        user.full_name = full_name
        user.save()

        return user


# Login serializer
User = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            email=data["email"],
            password=data["password"]
        )

        if not user:
            raise serializers.ValidationError("Invalid email or password")

        data["user"] = user
        return data

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()


# REGISTER

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Senhas não conferem")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')

        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


# LOGIN JWT


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError("Credenciais inválidas")

        data = super().validate({
            'username': email,
            'password': password
        })

        data['user'] = {
            'email': user.email,
            'full_name': user.username
        }

        return data

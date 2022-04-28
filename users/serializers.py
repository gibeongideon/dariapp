# from django.contrib.auth.models import User
from .models import User

# from .models import SetPasswordModel
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "phone_number",
            "referer_code",
            "first_name",
            "last_name",
            "email",
            "password",
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(), fields=["username", "email"]
            )
        ]


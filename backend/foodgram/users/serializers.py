from djoser.serializers import UserCreateSerializer, UserSerializer
from users.models import User


class UserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )
        lookup_field = "username"


class UserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
        )
        lookup_field = "username"

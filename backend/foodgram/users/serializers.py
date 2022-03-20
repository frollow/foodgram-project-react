from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from api.models import Recipe
from .models import Subscription, User


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

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

    def get_is_subscribed(self, following):
        if self.context.get(
            "request",
        ).user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=self.context.get("request").user, author=following
        ).exists()


class SubscriptionRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class ListSubscriptionSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )

    def get_recipes_count(self, following):
        return Recipe.objects.filter(author=following).count()

    def get_recipes(self, following):
        queryset = self.context.get("request")
        recipes_limit = queryset.query_params.get("recipes_limit")
        if not recipes_limit:
            return RecipeFollowingSerializer(
                following.follower.all(),
                many=True,
                context={"request": queryset},
            ).data
        return RecipeFollowingSerializer(
            following.follower.all()[: int(recipes_limit)],
            many=True,
            context={"request": queryset},
        ).data

    def get_is_subscribed(self, following):
        return Subscription.objects.filter(
            user=self.context.get("request").user, author=following
        ).exists()


class RecipeFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ("user", "author")

    def validate(self, data):
        get_object_or_404(User, username=data["author"])
        if self.context["request"].user == data["author"]:
            raise serializers.ValidationError("Сам на себя подписываешься!")
        if Subscription.objects.filter(
            user=self.context["request"].user, author=data["author"]
        ):
            raise serializers.ValidationError("Уже подписан")
        return data

    def to_representation(self, instance):
        return ListSubscriptionSerializer(
            instance.author,
            context={"request": self.context.get("request")},
        ).data

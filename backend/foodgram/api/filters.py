from django_filters import rest_framework as filters

from .models import Ingredient, Recipe


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Ingredient
        fields = ("name",)


class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name="tags__slug")
    is_favorited = filters.BooleanFilter(method="get_is_favorited")
    is_in_shopping_cart = filters.BooleanFilter(
        method="get_is_in_shopping_cart"
    )

    def get_is_favorited(self, queryset, value, name):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(recipe_favorite__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, value, name):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(
                recipe_shopping_cart__user=self.request.user
            )
        return queryset

    class Meta:
        model = Recipe
        fields = ("author", "tags")

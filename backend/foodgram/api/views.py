from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import (
    Tag,
    Recipe,
    Ingredient,
    Ingredient_in_recipe,
    Favorite,
    ShoppingCart,
)
from .serializers import (
    TagSerializer,
    RecipeSerializer,
    IngredientSerializer,
    FavoriteSerializer,
    ShoppingCartSerializer,
)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class FavoriteAndShoppingCartViewSet(APIView):
    def get(self, request, recipe_id):
        user = request.user
        data = {
            "user": user.id,
            "recipe": recipe_id,
        }
        serializer = self.serializer_class(
            data=data, context={"request": request}
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)

        self.obj.objects.get(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteViewSet(FavoriteAndShoppingCartViewSet):
    serializer_class = FavoriteSerializer
    obj = Favorite


class ShoppingCartViewSet(FavoriteAndShoppingCartViewSet):
    serializer_class = ShoppingCartSerializer
    obj = ShoppingCart


@api_view(["GET"])
def download_shopping_cart(request):
    user = request.user
    shoppingcart = user.user_shopping_cart.all()
    list = {}

    for item in shoppingcart:
        recipe = item.recipe
        ingredients = Ingredient_in_recipe.objects.filter(recipe=recipe)
        for ingredient in ingredients:
            amount = ingredient.amount
            name = ingredient.ingredient.name
            measurement_unit = ingredient.ingredient.measurement_unit
            if name not in list:
                list[name] = {
                    "measurement_unit": measurement_unit,
                    "amount": amount,
                }
            else:
                list[name]["amount"] = list[name]["amount"] + amount

    file_data = []
    for item in list:
        file_data.append(
            f'{item} - {list[item]["amount"]} '
            f'{list[item]["measurement_unit"]} \r\n'
        )

    response = HttpResponse(file_data, "Content-Type: text/plain")
    response["Content-Disposition"] = 'attachment; filename="wishlist.txt"'
    return response

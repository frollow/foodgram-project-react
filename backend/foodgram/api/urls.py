from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    TagViewSet,
    RecipeViewSet,
    IngredientViewSet,
    FavoriteViewSet,
    ShoppingCartViewSet,
    download_shopping_cart,
)


app_name = "api"

v1_router = DefaultRouter()
v1_router.register("tags", TagViewSet)
v1_router.register("recipes", RecipeViewSet)
v1_router.register("ingredients", IngredientViewSet)

urlpatterns = [
    path(
        "recipes/download_shopping_cart/",
        download_shopping_cart,
        name="download",
    ),
    path(
        "recipes/<int:recipe_id>/favorite/",
        FavoriteViewSet.as_view(),
        name="favorite",
    ),
    path(
        "recipes/<int:recipe_id>/shopping_cart/",
        ShoppingCartViewSet.as_view(),
        name="shopping_cart",
    ),
    path("", include("djoser.urls")),
    path("", include("djoser.urls.authtoken")),
    path("", include(v1_router.urls)),
]

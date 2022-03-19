from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, RecipesViewSet, TagsViewSet

router_v1 = DefaultRouter()

router_v1.register("tags", TagsViewSet, basename="tags")
router_v1.register("ingredients", IngredientViewSet, basename="ingredients")
router_v1.register("recipes", RecipesViewSet, basename="recipes")


urlpatterns = [
    path("", include(router_v1.urls)),
]

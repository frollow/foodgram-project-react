from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TagViewSet, RecipeViewSet, IngredientViewSet


app_name = "api"

v1_router = DefaultRouter()
v1_router.register("tags", TagViewSet)
v1_router.register("recipes", RecipeViewSet)
v1_router.register("ingredients", IngredientViewSet)

urlpatterns = [
    path("", include("djoser.urls")),
    path("", include("djoser.urls.authtoken")),
    path('', include(v1_router.urls)),
]

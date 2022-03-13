from django.urls import include, path
from rest_framework.routers import DefaultRouter


app_name = "api"
v1_router = DefaultRouter()


urlpatterns = [
    path("", include("djoser.urls")),
    path("", include('djoser.urls.authtoken'))
    # path("link/", include(v1_router.urls)),
]

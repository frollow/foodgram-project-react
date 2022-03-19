from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Subscription, User
from .paginator import VariablePageSizePaginator
from .serializers import (
    ListSubscriptionSerializer,
    SubscriptionSerializer,
    UserSerializer,
)


class CustomUserViewSet(UserViewSet):
    pagination_class = VariablePageSizePaginator

    @action(
        detail=False, methods=["GET"], permission_classes=(IsAuthenticated,)
    )
    def users(self, request):
        serializer = UserSerializer(
            super().get_queryset(), many=True, context={"request": request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=False, methods=["GET"], permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request, pk=None):
        subscriptions_list = self.paginate_queryset(
            User.objects.filter(following__user=request.user)
        )
        serializer = ListSubscriptionSerializer(
            subscriptions_list, many=True, context={"request": request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=["POST", "DELETE"],
        permission_classes=(IsAuthenticated,),
    )
    def subscribe(self, request, id):
        if request.method != "POST":
            subscription = get_object_or_404(
                Subscription,
                author=get_object_or_404(User, id=id),
                user=request.user,
            )
            self.perform_destroy(subscription)
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = SubscriptionSerializer(
            data={
                "user": request.user.id,
                "author": get_object_or_404(User, id=id).id,
            },
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

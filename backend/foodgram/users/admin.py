from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    """
    Параметры отображения модели User (пользователи)
    в интерфейсе администратора.
    """

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_subscribed",
        "role",
    )
    search_fields = ("username", "role")
    list_filter = ("role",)
    empty_value_display = "-пусто-"
    list_editable = ("role",)


admin.site.register(User, UserAdmin)

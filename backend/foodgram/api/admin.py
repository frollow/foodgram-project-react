from django.contrib import admin

from .models import (
    Favorite,
    Ingredient,
    IngredientInRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    list_filter = ("name",)


class TabularInlineIngredient(admin.TabularInline):
    model = IngredientInRecipe


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "favorited")
    list_filter = ("author", "name", "tags")
    exclude = ("ingredients",)
    inlines = [TabularInlineIngredient]

    def favorited(self, obj):
        favorited_count = Favorite.objects.filter(recipe=obj).count()
        return favorited_count

    favorited.short_description = "В избранном"


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe")


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe")


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)

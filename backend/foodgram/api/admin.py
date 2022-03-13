from django.contrib import admin

from .models import Tag, Ingredient, Ingredient_in_recipe, Recipe


class TagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "color",
        "slug",
    )
    empty_value_display = "-пусто-"


admin.site.register(Tag, TagAdmin)


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "measurement_unit",
    )
    empty_value_display = "-пусто-"


admin.site.register(Ingredient, IngredientAdmin)


class Ingredient_in_recipeInline(admin.StackedInline):
    model = Recipe.ingredients.through
    extra = 0


class Ingredient_in_recipeAdmin(admin.ModelAdmin):
    inlines = (Ingredient_in_recipeInline,)


admin.site.register(Ingredient_in_recipe, Ingredient_in_recipeAdmin)


class RecipeAdmin(admin.ModelAdmin):
    inlines = (Ingredient_in_recipeInline,)
    list_display = ("name", "author", "text", "cooking_time")
    exclude = ("ingredients",)
    empty_value_display = "-пусто-"


admin.site.register(Recipe, RecipeAdmin)

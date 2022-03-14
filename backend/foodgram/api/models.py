from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Exists, OuterRef, Value

from users.models import User


class RecipeQueryset(models.QuerySet):
    def annotate_user_flags(self, user):
        if user.is_anonymous:
            return self.annotate(
                is_favorited=Value(False, output_field=models.BooleanField()),
                is_in_shopping_cart=Value(
                    False, output_field=models.BooleanField()
                ),
            )
        return self.annotate(
            is_favorited=Exists(
                Favorite.objects.filter(user=user, recipe__pk=OuterRef("pk"))
            ),
            is_in_shopping_cart=Exists(
                ShoppingCart.objects.filter(
                    user=user, recipe__pk=OuterRef("pk")
                )
            ),
        )


class Tag(models.Model):
    name = models.CharField(
        max_length=200, null=True, unique=True, verbose_name="Тег"
    )
    color = models.CharField(
        max_length=200, null=True, unique=True
    )
    slug = models.SlugField(
        max_length=200, null=True, unique=True
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=199,
        null=True,
        unique=True,
        verbose_name="Название",
    )
    measurement_unit = models.CharField(
        max_length=50,
        verbose_name="Ед. измерения",
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipes"
    )
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="api/images/")
    text = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient, through="IngredientInRecipe"
    )
    tags = models.ManyToManyField(Tag, through="TagsRecipe")
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, "Время приготовления должно быть больше 0")
        ]
    )
    objects = RecipeQueryset.as_manager()

    class Meta:
        ordering = ("-pk",)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name


class TagsRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Тег чека"
        verbose_name_plural = "Теги чека"


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name="Ингредиент в рецепте",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
        related_name="recipe_ingredients",
    )
    amount = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, "Количество ингредиента должно быть больше 0")
        ]
    )

    class Meta:
        verbose_name = "Количество ингредиента"
        verbose_name_plural = "Количество ингредиентов"
        constraints = [
            models.UniqueConstraint(
                fields=["ingredient", "recipe"], name="unique_ingredient"
            )
        ]

    def __str__(self):
        return f"{self.ingredient} in {self.recipe}"


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_favorite",
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="recipe_favorite",
        verbose_name="Избранный рецепт",
    )
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
        default_related_name = "favorit"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique_favorite"
            )
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_shopping_cart",
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="recipe_shopping_cart",
        verbose_name="рецепт в корзине",
    )
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Покупка"
        verbose_name_plural = "Покупки"
        default_related_name = "shoplist"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique_shopping"
            )
        ]

    def __str__(self):
        return f"{self.recipe} в корзине у {self.user}"

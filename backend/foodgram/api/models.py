from colorfield.fields import ColorField
from django.db import models
from django.urls import reverse
from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Название тега",
        help_text="Название тега",
    )
    color = ColorField(default="#FF0000")
    slug = models.SlugField(
        unique=True,
        verbose_name="Slug для тега",
        help_text="Slug для тега",
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Tag_detail", kwargs={"pk": self.pk})


class Ingredient(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Ингридиент",
        help_text="Ингридиенты",
    )
    measurement_unit = models.CharField(
        max_length=20,
        verbose_name="Единица измерения",
        help_text="Единица измерения",
    )

    class Meta:
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Ingredient_detail", kwargs={"pk": self.pk})


class Ingredient_in_recipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="ingredient_in_recipe",
        null=True,
        verbose_name="Ингредиент в рецепте",
        help_text="Ингредиент в рецепте",
    )
    amount = models.SmallIntegerField(
        default=0,
        blank=False,
        null=False,
        verbose_name="Количество",
        help_text="Количество",
    )

    class Meta:
        verbose_name = "Ингредиент в рецепте"
        verbose_name_plural = "Ингредиенты в рецепте"

    def get_absolute_url(self):
        return reverse("Ingredient_detail", kwargs={"pk": self.pk})


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        related_name="recipe",
        verbose_name="Теги",
        help_text="Теги",
    )
    name = models.CharField(
        max_length=256,
        verbose_name="Название рецепта",
        help_text="Название рецепта",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipe",
        verbose_name="Автор",
    )
    ingredients = models.ManyToManyField(
        Ingredient_in_recipe,
        related_name="recipe",
        verbose_name="Ингридиенты",
        help_text="Ингридиенты",
    )
    text = models.TextField(
        verbose_name="Описание",
        help_text="Описание",
    )
    cooking_time = models.SmallIntegerField(
        default=0,
        blank=False,
        null=False,
        verbose_name="Общее время приготовления",
        help_text="Общее время приготовления",
    )
    image = models.ImageField("Картинка", upload_to="images/", blank=True)

    class Meta:
        verbose_name = "Pецепт"
        verbose_name_plural = "Pецепт"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Recipe_detail", kwargs={"pk": self.pk})


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

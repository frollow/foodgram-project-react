from colorfield.fields import ColorField
from django.db import models
from django.urls import reverse


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
        verbose_name = "Ingredient"
        verbose_name_plural = "Ingredients"

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
        verbose_name="Ингридиент в рецепте",
        help_text="Ингридиент в рецепте",
    )
    amount = models.SmallIntegerField(
        default=0,
        blank=False,
        null=False,
        verbose_name="Количество",
        help_text="Количество",
    )

    class Meta:
        verbose_name = "Ingredient"
        verbose_name_plural = "Ingredients"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Ingredient_detail", kwargs={"pk": self.pk})


class Recipe(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Название рецепта",
        help_text="Название рецепта",
    )
    ingredients = models.ManyToManyField(
        Ingredient_in_recipe,
        related_name="recipe",
        verbose_name="Ингридиенты",
        help_text="Ингридиенты",
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="recipe",
        verbose_name="Теги",
        help_text="Теги",
    )
    text = models.TextField(
        verbose_name='Описание',
        help_text='Описание',
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

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class LikedRecipe(models.Model):
    LIKED_TYPES = (
        ('L', 'Like'),
        ('B', 'Bookmark'),
    )
    user = models.ForeignKey('Author', on_delete=models.CASCADE, verbose_name="Пользователь")
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, verbose_name="Рецепт")
    liked_type = models.CharField(max_length=1, choices=LIKED_TYPES, verbose_name="Тип")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    class Meta:
        verbose_name = 'понравившийся рецепт'
        verbose_name_plural = 'понравившиеся рецепты'
        ordering = ['user', 'recipe']

    def __str__(self):
        return f"{str(self.user)} - {str(self.recipe)}"


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fathers_name = models.CharField(max_length=500, blank=True, null=True, verbose_name="Отчество")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    description = models.TextField(blank=True, null=True, verbose_name="О себе")
    photo = models.ImageField(upload_to="photos/users/%Y/%m/%d/", blank=True, null=True, verbose_name="Фото")
    slug = models.SlugField(max_length=255, unique=True)
    liked_recipes = models.ManyToManyField('Recipe', through=LikedRecipe, related_name='liked',
                                           verbose_name="Понравившиеся рецепты")
    my_exceptions = models.ManyToManyField('Product', blank=True, verbose_name="Исключения")
    liked_authors = models.ManyToManyField('self', blank=True, verbose_name="Любимые авторы")

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['user']

    def __str__(self):
        return f"{self.user} {self.slug}"


class Recipe(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(verbose_name="Описание")
    cooking_time = models.DurationField(verbose_name="Время приготовления")
    calories = models.PositiveIntegerField(default=0, verbose_name="Калории")
    num_of_servings = models.PositiveSmallIntegerField(verbose_name="Кол-во порций")
    finished_product_weight = models.PositiveSmallIntegerField(verbose_name="Итоговый вес")
    status = models.BooleanField(default=False, verbose_name="Опубликован")
    date_of_creation = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    edit_date = models.DateTimeField(auto_now=True, verbose_name="Дата редактирования")
    num_of_stars = models.PositiveIntegerField(default=0, verbose_name="Звезд")
    num_of_comments = models.PositiveIntegerField(default=0, verbose_name="Коментариев")
    num_of_bookmarks = models.PositiveIntegerField(default=0, verbose_name="Закладок")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    categories = models.ManyToManyField('Category', verbose_name="Категория")

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'
        ordering = ['id']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipe', kwargs={'recipe_slug': self.slug})


class RecipePhoto(models.Model):
    photo = models.ImageField(upload_to="photos/recipe/%Y/%m/%d/", verbose_name="Фото")
    index = models.PositiveSmallIntegerField(verbose_name="Номер")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="Рецепт")

    class Meta:
        verbose_name = 'Фото рецепта'
        verbose_name_plural = 'Фото рецепта'
        ordering = ['recipe']

    def __str__(self):
        return f"id({self.pk}) {self.index} - {self.photo}"


class RecipeStep(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    index = models.PositiveSmallIntegerField(verbose_name="Номер")
    photo = models.ImageField(upload_to="photos/recipe/%Y/%m/%d/", verbose_name="Фото")
    description = models.TextField(verbose_name="Описание")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="Рецепт")

    class Meta:
        verbose_name = 'Шаг рецепта'
        verbose_name_plural = 'Шаги рецепта'
        ordering = ['recipe', 'index']

    def __str__(self):
        return f"id({self.pk}) {self.index}. {self.title}"


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    photo = models.ImageField(upload_to="photos/category/%Y/%m/%d/", verbose_name="Фото")
    parent_category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True,
                                        verbose_name="Родительская категория")
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    is_essential = models.BooleanField(default=True, verbose_name="Основной")
    quantity = models.PositiveSmallIntegerField(verbose_name="Количество")
    index = models.PositiveSmallIntegerField(verbose_name="Номер в списке")
    main_ingredient = models.ForeignKey('RecipeIngredient', on_delete=models.CASCADE, blank=True, null=True,
                                        verbose_name="Главный ингридиент")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="Рецепт")
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name="Продукт")

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['recipe', 'index']

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    photo = models.ImageField(upload_to="photos/product/%Y/%m/%d/", verbose_name="Фото")
    product_type = models.ForeignKey('ProductType', on_delete=models.CASCADE, verbose_name="Тип продукта")
    slug = models.SlugField(max_length=255, unique=True)
    calories = models.PositiveIntegerField(verbose_name="Калории")
    fat = models.FloatField(verbose_name="Жиры")
    proteins = models.FloatField(verbose_name="Белки")
    carbohydrates = models.FloatField(verbose_name="Углеводы")

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['name']

    def __str__(self):
        return self.name


class ProductType(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    photo = models.ImageField(upload_to="photos/product/%Y/%m/%d/", verbose_name="Фото")
    slug = models.SlugField(max_length=255, unique=True)
    parent_type = models.ForeignKey('ProductType', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Родительский тип")

    class Meta:
        verbose_name = 'тип продукта'
        verbose_name_plural = 'типы продуктов'
        ordering = ['name']

    def __str__(self):
        return self.name


class RecipeComment(models.Model):
    text = models.TextField()
    date_of_creation = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    edit_date = models.DateTimeField(auto_now=True, verbose_name="Дата редактирования")
    index = models.PositiveSmallIntegerField(verbose_name="Номер")
    parent_comment = models.ForeignKey('RecipeComment', on_delete=models.CASCADE, blank=True, null=True,
                                       verbose_name="Родительский комментарий")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="Рецепт")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор комментария")

    def __str__(self):
        return f"{self.index}. {self.text[:15]} - {self.user}"

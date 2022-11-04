from django.db import models


class LikedRecipe(models.Model):
    LIKED_TYPES = (
        ('L', 'Like'),
        ('B', 'Bookmark'),
    )
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    liked_type = models.CharField(max_length=1, choices=LIKED_TYPES)
    date = models.DateTimeField(auto_now_add=True)


class User(models.Model):
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500, blank=True, null=True)
    fathers_name = models.CharField(max_length=500, blank=True, null=True)
    login = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to="photos/users/%Y/%m/%d/", blank=True, null=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True)
    liked_recipes = models.ManyToManyField('Recipe', through=LikedRecipe, related_name='liked')
    my_exceptions = models.ManyToManyField('Product')
    liked_authors = models.ManyToManyField('self')


class Recipe(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    cooking_time = models.DurationField()
    calories = models.PositiveIntegerField()
    num_of_servings = models.PositiveSmallIntegerField()
    finished_product_weight = models.PositiveSmallIntegerField()
    status = models.BooleanField(default=False)
    date_of_creation = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    num_of_stars = models.PositiveIntegerField()
    num_of_comments = models.PositiveIntegerField()
    num_of_bookmarks = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField('Category')


class RecipePhoto(models.Model):
    photo = models.ImageField(upload_to="photos/recipe/%Y/%m/%d/")
    index = models.PositiveSmallIntegerField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class RecipeStep(models.Model):
    title = models.CharField(max_length=255)
    index = models.PositiveSmallIntegerField()
    photo = models.ImageField(upload_to="photos/recipe/%Y/%m/%d/")
    description = models.TextField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    photo = models.ImageField(upload_to="photos/category/%Y/%m/%d/")
    parent_category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)


class RecipeIngredient(models.Model):
    comment = models.TextField(blank=True, null=True)
    is_essential = models.BooleanField(default=True)
    quantity = models.PositiveSmallIntegerField()
    index = models.PositiveSmallIntegerField()
    main_ingredient = models.ForeignKey('RecipeIngredient', on_delete=models.CASCADE, blank=True, null=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    photo = models.ImageField(upload_to="photos/product/%Y/%m/%d/")
    product_type = models.ForeignKey('ProductType', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True)


class ProductType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    photo = models.ImageField(upload_to="photos/product/%Y/%m/%d/")
    slug = models.SlugField(max_length=255, unique=True)


class RecipeComment(models.Model):
    text = models.TextField()
    date_of_creation = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    index = models.PositiveSmallIntegerField()
    parent_comment = models.ForeignKey('RecipeComment', on_delete=models.CASCADE, blank=True, null=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

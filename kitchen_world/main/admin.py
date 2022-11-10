from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import User, Recipe, Product, ProductType, Category, LikedRecipe, RecipePhoto, RecipeStep, RecipeIngredient

# Register your models here.

admin.site.site_title = 'Kitchen World'
admin.site.site_header = 'Админ-панель Kitchen World'


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'get_html_photo', 'login', 'password', 'email', 'registration_date')
    list_display_links = ('id', 'first_name')
    search_fields = ('first_name', 'login')
    prepopulated_fields = {'slug': ('first_name', 'last_name', 'fathers_name')}
    fields = ('id', 'last_name', 'first_name', 'fathers_name', 'slug', 'login', 'password', 'email', 'phone',
              'description', 'get_html_photo', 'photo', 'registration_date', 'my_exceptions', 'liked_authors',
              'get_my_recipe', 'get_liked_recipe', 'get_bookmark_recipe')
    readonly_fields = ('id', 'get_html_photo', 'registration_date', 'liked_recipes', 'my_exceptions', 'liked_authors',
                       'get_my_recipe', 'get_liked_recipe', 'get_bookmark_recipe')

    def get_html_photo(self, obj):
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' height=50>")

    get_html_photo.short_description = "Фото"

    def get_my_recipe(self, obj):
        all_recipe = obj.recipe_set.all()
        recipes_str = ''
        for r in all_recipe:
            recipes_str += str(r) + '\n'
        return recipes_str

    get_my_recipe.short_description = "Рецепты автора"

    def get_liked_recipe(self, obj):
        liked_recipes = obj.liked_recipes.filter(likedrecipe__liked_type='L')
        recipes_str = ''
        for r in liked_recipes:
            recipes_str += str(r) + '\n'
        return recipes_str

    get_liked_recipe.short_description = "Понравившиеся"

    def get_bookmark_recipe(self, obj):
        liked_recipes = obj.liked_recipes.filter(likedrecipe__liked_type='B')
        recipes_str = ''
        for r in liked_recipes:
            recipes_str += str(r) + '\n'
        return recipes_str

    get_bookmark_recipe.short_description = "Закладки"


admin.site.register(User, UserAdmin)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'status', 'date_of_creation', 'edit_date')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'id')
    prepopulated_fields = {'slug': ('title',)}
    fields = ('id', 'title', 'slug', 'get_all_recipe_photo', 'description', ('cooking_time', 'calories',
              'num_of_servings', 'finished_product_weight'), 'status', 'user', 'categories', 'get_all_recipe_ingredient',
              'get_all_recipe_step', ('date_of_creation', 'edit_date'), ('num_of_stars',
              'num_of_comments', 'num_of_bookmarks'))
    readonly_fields = ('id', 'date_of_creation', 'edit_date', 'calories', 'num_of_stars', 'num_of_comments', 'num_of_bookmarks',
                       'user', 'get_all_recipe_photo', 'get_all_recipe_ingredient', 'get_all_recipe_step')

    def get_all_recipe_photo(self, obj):
        photos_html = ''
        for p in RecipePhoto.objects.filter(recipe=obj.id).order_by('index'):
            photos_html += f'<a href="/admin/main/recipephoto/{p.id}/change/"><img style="margin: 5px"' \
                           f' src="{p.photo.url}" height=50></a>'
        return mark_safe(photos_html)
    get_all_recipe_photo.short_description = "Фото рецепта"

    def get_all_recipe_ingredient(self, obj):
        ingredients_html = ''
        for i in RecipeIngredient.objects.filter(recipe=obj.id).order_by('index'):
            ingredients_html += f'<div>' \
                                f'<a href="/admin/main/recipeingredient/{i.id}/change/">{i.product}</a> ' \
                                f'<b>{i.quantity}</b>' \
                                f'<p>{i.comment}</p>' \
                                f'<p>{i.main_ingredient}</p>' \
                                f'</div><hr>'
        return mark_safe(ingredients_html)
    get_all_recipe_ingredient.short_description = "Ингредиенты"

    def get_all_recipe_step(self, obj):
        steps_html = ''
        for s in RecipeStep.objects.filter(recipe=obj.id).order_by('index'):
            steps_html += f'<div>' \
                          f'<a href="/admin/main/recipestep/{s.id}/change/">{s.title}</a>' \
                          f'<img style="margin: 5px" src="{s.photo.url}" height=50>' \
                          f'<p>{s.description}</p>' \
                          f'</div>'
        return mark_safe(steps_html)
    get_all_recipe_step.short_description = "Шаги рецепта"


admin.site.register(Recipe, RecipeAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_html_photo')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}
    fields = ('id', 'name', 'slug', 'description', 'get_html_photo', 'photo', 'product_type', 'calories', 'fat',
              'proteins', 'carbohydrates')
    readonly_fields = ('id', 'get_html_photo')

    def get_html_photo(self, obj):
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' height=50>")

    get_html_photo.short_description = "Фото"


admin.site.register(Product, ProductAdmin)


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_html_photo')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}
    fields = ('id', 'name', 'slug', 'description', 'get_html_photo', 'photo', 'parent_type')
    readonly_fields = ('id', 'get_html_photo')

    def get_html_photo(self, obj):
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' height=50>")

    get_html_photo.short_description = "Фото"


admin.site.register(ProductType, ProductTypeAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_html_photo', 'parent_category')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}
    fields = ('id', 'name', 'slug', 'description', 'get_html_photo', 'photo', 'parent_category')
    readonly_fields = ('id', 'get_html_photo',)

    def get_html_photo(self, obj):
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' height=50>")

    get_html_photo.short_description = "Фото"


admin.site.register(Category, CategoryAdmin)


class LikedRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe', 'liked_type', 'date')
    list_display_links = ('id', 'user', 'recipe')
    search_fields = ('id', 'user', 'recipe')
    fields = ('id', 'user', 'recipe', 'liked_type', 'date')
    readonly_fields = ('id', 'date')


admin.site.register(LikedRecipe, LikedRecipeAdmin)


class RecipePhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_html_photo', 'index', 'recipe')
    list_display_links = ('id', 'get_html_photo')
    search_fields = ('id', 'index', 'recipe')
    fields = ('id', 'get_html_photo', 'photo', 'index', 'recipe')
    readonly_fields = ('id', 'get_html_photo')

    def get_html_photo(self, obj):
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' height=50>")

    get_html_photo.short_description = "Фото"


admin.site.register(RecipePhoto, RecipePhotoAdmin)


class RecipeStepAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'index', 'recipe')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title')
    fields = ('id', 'title', 'index', 'get_html_photo', 'photo', 'description', 'recipe')
    readonly_fields = ('id', 'get_html_photo')

    def get_html_photo(self, obj):
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' height=50>")

    get_html_photo.short_description = "Фото"


admin.site.register(RecipeStep, RecipeStepAdmin)


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'is_essential', 'recipe', 'main_ingredient')
    list_display_links = ('id', 'product')
    search_fields = ('id',)
    fields = ('id', 'product', 'quantity', 'is_essential', 'index', 'main_ingredient', 'comment', 'recipe')
    readonly_fields = ('id',)


admin.site.register(RecipeIngredient, RecipeIngredientAdmin)

from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import User, Recipe, Product, ProductType, Category, LikedRecipe

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
            return mark_safe(f"<img src='{obj.photo.url}' width=50>")

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
    fields = ('id', 'title', 'slug', 'description', 'cooking_time', 'calories', 'num_of_servings',
              'finished_product_weight', 'status', 'user', 'categories', 'date_of_creation', 'edit_date',
              'num_of_stars', 'num_of_comments', 'num_of_bookmarks')
    readonly_fields = ('id', 'date_of_creation', 'edit_date', 'num_of_stars', 'num_of_comments', 'num_of_bookmarks',
                       'user')


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
            return mark_safe(f"<img src='{obj.photo.url}' width=50>")
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
            return mark_safe(f"<img src='{obj.photo.url}' width=50>")
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
            return mark_safe(f"<img src='{obj.photo.url}' width=50>")
    get_html_photo.short_description = "Фото"


admin.site.register(Category, CategoryAdmin)


class LikedRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe', 'liked_type', 'date')
    list_display_links = ('id', 'user', 'recipe')
    search_fields = ('id', 'user', 'recipe')
    fields = ('id', 'user', 'recipe', 'liked_type', 'date')
    readonly_fields = ('id', 'date')


admin.site.register(LikedRecipe, LikedRecipeAdmin)

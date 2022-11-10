import json
import os

import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kitchen_world.settings")
django.setup()

from django.contrib.auth.models import User
from main.models import Product, ProductType, Category, Author, Recipe, RecipePhoto, RecipeStep, RecipeIngredient, \
    RecipeComment

print('hello')


def get_all_products() -> list:
    all_product = Product.objects.all()
    arr = []
    for p in all_product:
        arr.append({'id': p.id,
                    'name': p.name,
                    'description': p.description,
                    'photo': p.photo.name,
                    'product_type': p.product_type.id,
                    'slug': p.slug,
                    'calories': p.calories,
                    'fat': p.fat,
                    'proteins': p.proteins,
                    'carbohydrates': p.carbohydrates,
                    })
    return arr


def get_all_product_types() -> list:
    all_product_type = ProductType.objects.all()
    arr = []
    for p in all_product_type:
        arr.append({'id': p.id,
                    'name': p.name,
                    'description': p.description,
                    'photo': p.photo.name,
                    'slug': p.slug,
                    'parent_type': p.parent_type.id if not (p.parent_type is None) else p.parent_type
                    })
    return arr


def get_all_categories() -> list:
    all_categories = Category.objects.all()
    arr = []
    for c in all_categories:
        arr.append({'id': c.id,
                    'name': c.name,
                    'description': c.description,
                    'photo': c.photo.name,
                    'parent_category': c.parent_category.id if not (
                            c.parent_category is None) else c.parent_category,
                    'slug': c.slug
                    })
    return arr


def get_all_users() -> list:
    all_users = User.objects.all()
    arr = []
    for u in all_users:
        arr.append({'id': u.id,
                    'password': u.password,
                    'last_login': str(u.last_login) if not(u.last_login is None) else None,
                    'is_superuser': u.is_superuser,
                    'username': u.username,
                    'last_name': u.last_name,
                    'email': u.email,
                    'is_staff': u.is_staff,
                    'is_active': u.is_active,
                    'date_joined': str(u.date_joined),
                    'first_name': u.first_name,
                    })
    return arr


def get_all_authors() -> list:
    all_authors = Author.objects.all()
    arr = []
    for a in all_authors:
        arr.append({'id': a.id,
                    'user': a.user.id,
                    'fathers_name': a.fathers_name,
                    'phone': a.phone,
                    'description': a.description,
                    'photo': a.photo.name,
                    'slug': a.slug,
                    })
    return arr


def get_all_recipes() -> list:
    all_recipe = Recipe.objects.all()
    arr = []
    for r in all_recipe:
        categories = r.categories.all()
        cat_ids = []
        for c in categories:
            cat_ids.append(c.id)
        arr.append({'id': r.id,
                    'title': r.title,
                    'slug': r.slug,
                    'description': r.description,
                    'cooking_time': r.cooking_time.total_seconds(),
                    'calories': r.calories,
                    'num_of_servings': r.num_of_servings,
                    'finished_product_weight': r.finished_product_weight,
                    'status': r.status,
                    'date_of_creation': str(r.date_of_creation),
                    'edit_date': str(r.edit_date),
                    'num_of_stars': r.num_of_stars,
                    'num_of_comments': r.num_of_comments,
                    'num_of_bookmarks': r.num_of_bookmarks,
                    'user': r.user.id,
                    'categories': cat_ids
                    })
    return arr


def get_all_recipe_photos() -> list:
    all_recipe_photos = RecipePhoto.objects.all()
    arr = []
    for rp in all_recipe_photos:
        arr.append({'id': rp.id,
                    'photo': rp.photo.name,
                    'index': rp.index,
                    'recipe': rp.recipe.id,
                    })
    return arr


def get_all_recipe_steps() -> list:
    all_recipe_steps = RecipeStep.objects.all()
    arr = []
    for rs in all_recipe_steps:
        arr.append({'id': rs.id,
                    'title': rs.title,
                    'index': rs.index,
                    'photo': rs.photo.name,
                    'description': rs.description,
                    'recipe': rs.recipe.id,
                    })
    return arr


def get_all_recipe_ingredients() -> list:
    all_recipe_ingredients = RecipeIngredient.objects.all()
    arr = []
    for ri in all_recipe_ingredients:
        arr.append({'id': ri.id,
                    'comment': ri.comment,
                    'is_essential': ri.is_essential,
                    'quantity': ri.quantity,
                    'index': ri.index,
                    'main_ingredient': ri.main_ingredient.id if not (
                            ri.main_ingredient is None) else ri.main_ingredient,
                    'recipe': ri.recipe.id,
                    'product': ri.product.id,
                    })
    return arr


def get_all_recipe_comments() -> list:
    all_recipe_comments = RecipeComment.objects.all()
    arr = []
    for rc in all_recipe_comments:
        arr.append({'id': rc.id,
                    'text': rc.text,
                    'date_of_creation': str(rc.date_of_creation),
                    'edit_date': str(rc.edit_date),
                    'index': rc.index,
                    'parent_comment': rc.parent_comment.id if not (
                            rc.parent_comment is None) else rc.parent_comment,
                    'recipe': rc.recipe.id,
                    'user': rc.user.id
                    })
    return arr


def write_to_jsonfile(values: list, file_name: str = "values.json"):
    with open(file_name, "w") as wf:
        json.dump(values, wf)


if __name__ == '__main__':
    write_to_jsonfile(get_all_categories(), "../temp/categories.json")
    write_to_jsonfile(get_all_products(), "../temp/products.json")
    write_to_jsonfile(get_all_product_types(), "../temp/product_types.json")
    write_to_jsonfile(get_all_users(), "../temp/users.json")
    write_to_jsonfile(get_all_authors(), "../temp/authors.json")
    write_to_jsonfile(get_all_recipes(), "../temp/recipes.json")
    write_to_jsonfile(get_all_recipe_comments(), "../temp/recipe_comments.json")
    write_to_jsonfile(get_all_recipe_photos(), "../temp/recipe_photos.json")
    write_to_jsonfile(get_all_recipe_steps(), "../temp/recipe_steps.json")
    write_to_jsonfile(get_all_recipe_ingredients(), "../temp/recipe_ingredients.json")


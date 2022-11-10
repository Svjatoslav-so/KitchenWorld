import json
import os
from datetime import timedelta

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kitchen_world.settings")
django.setup()

from main.models import Category, Product, ProductType, User, Recipe, RecipePhoto, RecipeStep, RecipeIngredient, \
    RecipeComment


def import_categories():
    try:
        with open('temp/categories.json', 'r') as fr:
            categories = json.load(fr)

        print("len- ", len(categories))
        for c in categories:
            try:
                parent_category = Category.objects.get(pk=c['parent_category'])
            except:
                parent_category = None
            cat = Category(id=c['id'],
                           name=c['name'],
                           description=c['description'],
                           photo=c['photo'],
                           parent_category=parent_category,
                           slug=c['slug'])
            cat.save()
    except Exception as e:
        print(e)


def import_products():
    try:
        with open('temp/products.json', 'r') as fr:
            products = json.load(fr)
        for p in products:
            prod = Product(id=p['id'],
                           name=p['name'],
                           description=p['description'],
                           photo=p['photo'],
                           product_type=ProductType.objects.get(pk=p['product_type']),
                           slug=p['slug'],
                           calories=p['calories'],
                           fat=p['fat'],
                           proteins=p['proteins'],
                           carbohydrates=p['carbohydrates'])
            prod.save()
    except Exception as e:
        print(e)


def import_product_types():
    try:

        with open('temp/product_types.json', 'r') as fr:
            product_types = json.load(fr)
        for pt in product_types:
            try:
                parent_type = ProductType.objects.get(pk=pt['parent_type'])
            except:
                parent_type = None
            prod_type = ProductType(id=pt['id'],
                                    name=pt['name'],
                                    description=pt['description'],
                                    photo=pt['photo'],
                                    slug=pt['slug'],
                                    parent_type=parent_type)
            prod_type.save()
    except Exception as e:
        print(e)


def import_users():
    try:
        with open('temp/users.json', 'r') as fr:
            users = json.load(fr)
        for u in users:
            user = User(id=u['id'],
                        first_name=u['first_name'],
                        last_name=u['last_name'],
                        fathers_name=u['fathers_name'],
                        login=u['login'],
                        password=u['password'],
                        email=u['email'],
                        phone=u['phone'],
                        description=u['description'],
                        photo=u['photo'],
                        registration_date=u['registration_date'],
                        slug=u['slug'])
            user.save()
    except Exception as e:
        print(e)


def import_recipes():
    try:
        with open('temp/recipes.json', 'r') as fr:
            recipes = json.load(fr)
        for r in recipes:
            recipe = Recipe(id=r['id'],
                            title=r['title'],
                            slug=r['slug'],
                            description=r['description'],
                            cooking_time=timedelta(seconds=r['cooking_time']),
                            calories=r['calories'],
                            num_of_servings=r['num_of_servings'],
                            finished_product_weight=r['finished_product_weight'],
                            status=r['status'],
                            date_of_creation=r['date_of_creation'],
                            edit_date=r['edit_date'],
                            num_of_stars=r['num_of_stars'],
                            num_of_comments=r['num_of_comments'],
                            num_of_bookmarks=r['num_of_bookmarks'],
                            user=User.objects.get(pk=r['user']))
            recipe.save()
            for c in r['categories']:
                category = Category.objects.get(pk=c)
                recipe.categories.add(category)

    except Exception as e:
        print(e)


def import_recipe_photos():
    try:
        with open('temp/recipe_photos.json', 'r') as fr:
            recipe_photos = json.load(fr)
        for rp in recipe_photos:
            recipe_photo = RecipePhoto(id=rp['id'],
                                       photo=rp['photo'],
                                       index=rp['index'],
                                       recipe=Recipe.objects.get(pk=rp['recipe'])
                                       )
            recipe_photo.save()

    except Exception as e:
        print(e)


def import_recipe_steps():
    try:
        with open('temp/recipe_steps.json', 'r') as fr:
            recipe_steps = json.load(fr)
        for rs in recipe_steps:
            recipe_step = RecipeStep(id=rs['id'],
                                     title=rs['title'],
                                     index=rs['index'],
                                     photo=rs['photo'],
                                     description=rs['description'],
                                     recipe=Recipe.objects.get(pk=rs['recipe']),
                                     )
            recipe_step.save()

    except Exception as e:
        print(e)


def import_recipe_ingredients():
    try:
        with open('temp/recipe_ingredients.json', 'r') as fr:
            recipe_ingredients = json.load(fr)
        for ri in recipe_ingredients:
            try:
                main_ingredient = RecipeIngredient.objects.get(pk=ri['main_ingredient'])
            except:
                main_ingredient = None
            recipe_ingredient = RecipeIngredient(id=ri['id'],
                                                 comment=ri['comment'],
                                                 is_essential=ri['is_essential'],
                                                 quantity=ri['quantity'],
                                                 index=ri['index'],
                                                 main_ingredient=main_ingredient,
                                                 recipe=Recipe.objects.get(pk=ri['recipe']),
                                                 product=Product.objects.get(pk=ri['product']),
                                                 )
            recipe_ingredient.save()

    except Exception as e:
        print(e)


def import_recipe_comments():
    try:
        with open('temp/recipe_comments.json', 'r') as fr:
            recipe_comments = json.load(fr)
        for rc in recipe_comments:
            try:
                parent_comment = RecipeComment.objects.get(pk=rc['parent_comment'])
            except:
                parent_comment = None
            recipe_comment = RecipeComment(id=rc['id'],
                                           text=rc['text'],
                                           date_of_creation=rc['date_of_creation'],
                                           edit_date=rc['edit_date'],
                                           index=rc['index'],
                                           parent_comment=parent_comment,
                                           recipe=Recipe.objects.get(pk=rc['recipe']),
                                           user=User.objects.get(pk=rc['user'])
                                           )
            recipe_comment.save()

    except Exception as e:
        print(e)


if __name__ == '__main__':
    import_users()
    import_categories()
    import_recipes()
    import_recipe_comments()
    import_recipe_photos()
    import_recipe_steps()
    import_product_types()  # Важно, что сначала тип продукта, а потом уже сам продукт
    import_products()
    import_recipe_ingredients()

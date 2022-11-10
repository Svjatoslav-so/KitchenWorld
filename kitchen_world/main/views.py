from django.shortcuts import render

# Create your views here.
from .models import Recipe, RecipePhoto


def combine_recipes_and_photos(recipes) -> list[tuple]:
    combined_array = []
    for r in recipes:
        try:
            photo = RecipePhoto.objects.filter(recipe=r.id).order_by('index')[0]
        except:
            photo = None
        combined_array.append((r, photo))
    return combined_array


def index(request):
    new_recipe = Recipe.objects.all().order_by("-date_of_creation")[:5]
    print(new_recipe)

    best_recipe = Recipe.objects.all().order_by("-num_of_stars")[:5]
    print(best_recipe)

    context = {
        "sections": [
            ("NEW", combine_recipes_and_photos(new_recipe)),
            ("BEST", combine_recipes_and_photos(best_recipe))
        ]
    }

    return render(request, 'main/index.html', context=context)

from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy

from .forms import RegistrationUserForm, LoginUserForm
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


def login(request):
    context = {
        'action': 'login'
    }
    return render(request, 'main/login.html', context=context)


class LoginUser(LoginView):
    # form_class = AuthenticationForm
    form_class = LoginUserForm
    template_name = 'main/login.html'
    extra_context = {
        'action': 'login'
    }

    def get_success_url(self):
        return reverse_lazy('home')


def registration(request):
    if request.method == 'POST':
        form = RegistrationUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RegistrationUserForm()
    context = {
        'action': 'registration',
        'form': form
    }
    return render(request, 'main/login.html', context=context)


def logout_user(request):
    logout(request)
    return redirect('home')

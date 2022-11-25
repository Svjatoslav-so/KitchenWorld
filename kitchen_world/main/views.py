from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy

from .forms import RegistrationUserForm, LoginUserForm, EditProfileForm
from .models import Recipe, RecipePhoto


def is_auth(func):
    def check(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return redirect('login')

    return check


def combine_recipes_and_photos(recipes):
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


class LoginUser(LoginView):
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
            user = form.save()
            login(request, user)
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


@is_auth
def edit_profile(request):
    if request.method == "POST":
        print("POST", request.POST)
        form = EditProfileForm(request.POST)
        print('form', form)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            description = form.cleaned_data['description']
            user = request.user
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.author.description = description
            user.save()
            user.author.save()
    else:
        print("GET", request)
        form = EditProfileForm(
            {'first_name': request.user.first_name,
             'username': request.user.username,
             'email': request.user.email,
             'description': request.user.author.description,
             'last_name': request.user.last_name})
    context = {
        'form': form
    }
    return render(request, 'main/edit_profile.html', context=context)


def catalog(request):
    logout(request)
    return render(request, 'main/catalogue.html')

def recipe(request, recipe_slug):
    recp = get_object_or_404(Recipe, slug=recipe_slug)
    context = {'recipe': recp}
    return render(request, 'main/recipe.html', context=context)

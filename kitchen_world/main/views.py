from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max, Q, F
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.utils.text import slugify

from .forms import RegistrationUserForm, LoginUserForm, EditProfileForm
from .models import Recipe, RecipePhoto, Category, Author, RecipeComment, LikedRecipe


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
            author = Author.objects.create(user=user, slug=slugify(f'{user.username} {user.id}'))
            author.save()
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
        form = EditProfileForm(request.POST, request.FILES)
        print('form', form)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            description = form.cleaned_data['description']
            photo = form.cleaned_data['photo']
            try:
                check_user = User.objects.get(username=username)
            except ObjectDoesNotExist:
                check_user = None
            user = request.user
            if check_user is None or user == check_user:
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
                user.author.description = description
                if not (photo is None):
                    if user.author.photo:
                        user.author.photo.delete()
                        print("\nSUCCESSFULLY\n")
                    user.author.photo = photo
                print('input_photo', photo)
                print("author.photo", user.author.photo)
                user.save()
                user.author.save()
            else:
                form.add_error('username', 'Пользователь с таким именем уже существует.')
    else:
        print("GET", request)
        print("photo", request.user.author.photo)
        form = EditProfileForm(
            {'first_name': request.user.first_name,
             'username': request.user.username,
             'email': request.user.email,
             'description': request.user.author.description,
             'last_name': request.user.last_name,
             })
    context = {
        'form': form
    }
    return render(request, 'main/edit_profile.html', context=context)


def catalog(request):
    if request.method == "GET":
        print(request.GET)
        categor = request.GET.getlist("category")
        sort = request.GET.get("sort", "-num_of_stars")
        search = request.GET.get("search-input", "")
        print("CATEGOR", categor)
        print(len(categor))
        print("SEARCH", search)
        bool = (len(search) != 0)
        print(bool)
        print(len(search))

        print("SORT", sort)
        if len(categor) != 0 and len(search) != 0:
            recipes = []
            for c in categor:
                recipes = merge_cat(recipes, list(
                    Recipe.objects.filter(categories__name=c).filter(title__iregex=search).order_by(sort)))
        if len(categor) != 0 and len(search) == 0:
            recipes = []
            for c in categor:
                recipes = merge_cat(recipes, list(Recipe.objects.filter(categories__name=c).order_by(sort)))
        if len(categor) == 0 and len(search) != 0:
            recipes = []
            recipes = merge_cat(recipes, list(Recipe.objects.all().filter(title__iregex=search).order_by(sort)))
        if len(categor) == 0 and len(search) == 0:
            recipes = Recipe.objects.all().order_by(sort)
    else:
        recipes = Recipe.objects.all()
    if len(recipes) == 0:
        is_data = False
    else:
        is_data = True
    context = {
        'recipes': combine_recipes_and_photos(recipes),
        'category': Category.objects.filter(parent_category=None),
        'sub_category': Category.objects.all(),
        'selected_categories': categor,
        'selected_sort': sort,
        'curr_search': search,
        'is_data_exist': is_data
    }
    return render(request, 'main/catalogue.html', context=context)


def merge_cat(cat, cat_new):
    for c in cat_new:
        if not c in cat:
            cat.append(c)
    return cat


def recipe(request, recipe_slug):
    recp = get_object_or_404(Recipe, slug=recipe_slug)
    comments = RecipeComment.objects.filter(recipe=recp).filter(parent_comment=None)
    context = {
        'recipe': recp,
        'comments': comments,
    }
    return render(request, 'main/recipe.html', context=context)


def my_recipes(request):
    recipes = Recipe.objects.filter(user=request.user).filter(status=True)
    context = {
        'recipes': combine_recipes_and_photos(recipes),
        'active': 'Мои рецепты'
    }
    return render(request, 'main/my_profile.html', context=context)


def my_drafts(request):
    recipes = Recipe.objects.filter(user=request.user).filter(status=False)
    context = {
        'recipes': combine_recipes_and_photos(recipes),
        'active': 'Черновики'
    }
    return render(request, 'main/my_profile.html', context=context)


def my_liked(request):
    recipes = Recipe.objects.filter(likedrecipe__user=request.user.author, likedrecipe__liked_type='L')
    context = {
        'recipes': combine_recipes_and_photos(recipes),
        'active': 'Понравившиеся'
    }
    return render(request, 'main/my_profile.html', context=context)


def my_bookmarks(request):
    recipes = Recipe.objects.filter(likedrecipe__user=request.user.author, likedrecipe__liked_type='B')
    context = {
        'recipes': combine_recipes_and_photos(recipes),
        'active': 'Закладки'
    }
    return render(request, 'main/my_profile.html', context=context)


@is_auth
def add_comment(request, recipe_slug):
    if request.method == "POST":
        print(request.POST)
        parent_comment_id = request.POST.get("parent_comment_id", None)
        if parent_comment_id:
            try:
                parent_comment = RecipeComment.objects.get(pk=parent_comment_id)
            except ObjectDoesNotExist:
                parent_comment = None
        else:
            parent_comment = None
        text = request.POST.get("new_comment", "Очень хороший рецепт!!!")
        _recipe = get_object_or_404(Recipe, slug=recipe_slug)
        max_ = RecipeComment.objects.aggregate(max_index=Max('index', filter=Q(recipe=_recipe), default=0))
        print("max_index: ", max_["max_index"])
        new_comment = RecipeComment.objects.create(text=text, index=max_["max_index"] + 1, recipe=_recipe,
                                                   user=request.user, parent_comment=parent_comment)
        new_comment.save()
    return redirect("recipe", recipe_slug)


@is_auth
def delete_comment(request, recipe_slug, comment_id):
    if request.method == "POST":
        print(request.POST)
        comment = get_object_or_404(RecipeComment, pk=comment_id)
        if comment.user == request.user:
            comment.delete()
    return redirect("recipe", recipe_slug)


def stars_on(request):
    print("ON_STARS_Request: ", request)
    if request.method == "GET":
        try:
            like_type = request.GET.get("type")
            recipe_id = request.GET.get("id")
            print("type: ", like_type, "id: ", recipe_id)
            user = request.user.author
            _recipe = Recipe.objects.get(id=recipe_id)
            if like_type == 'L':
                _recipe.num_of_stars = F('num_of_stars') + 1
                _recipe.save(update_fields=["num_of_stars"])
            else:
                _recipe.num_of_bookmarks = F('num_of_bookmarks') + 1
                _recipe.save(update_fields=["num_of_bookmarks"])
            like = LikedRecipe(user=user, recipe=_recipe, liked_type=like_type)
            like.save()

            return HttpResponse("OK")
        except :
            return HttpResponse("FAIL")
    return HttpResponse("FAIL")


def stars_off(request):
    print("OFF_STARS_Request: ", request)
    if request.method == "GET":
        try:
            like_type = request.GET.get("type")
            recipe_id = request.GET.get("id")
            print("type: ", like_type, "id: ", recipe_id)
            user = request.user.author
            _recipe = Recipe.objects.get(id=recipe_id)
            if like_type == 'L':
                _recipe.num_of_stars = F('num_of_stars') - 1
                _recipe.save(update_fields=["num_of_stars"])
            else:
                _recipe.num_of_bookmarks = F('num_of_bookmarks') - 1
                _recipe.save(update_fields=["num_of_bookmarks"])
            LikedRecipe.objects.get(user=user, recipe=_recipe, liked_type=like_type).delete()

            return HttpResponse("OK")
        except :
            return HttpResponse("FAIL")
    return HttpResponse("FAIL")

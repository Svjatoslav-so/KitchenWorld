import datetime

from PIL import Image
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, InvalidPage
from django.db.models import Max, Q, F
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.text import slugify as django_slugify
from django.views.defaults import page_not_found

from .forms import RegistrationUserForm, LoginUserForm, EditProfileForm, ChangeUserPasswordForm, LoadMainPhotoForm, \
    LoadStepPhotoForm
from .models import Recipe, RecipePhoto, Category, Author, RecipeComment, LikedRecipe, Product, ProductType, \
    RecipeStep, RecipeIngredient

CART_ON_PAGE = 9

alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}


def slugify(s):
    """
    Overriding django slugify that allows to use russian words as well.
    """
    return django_slugify(''.join(alphabet.get(w, w) for w in s.lower()))


def is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'


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
    _new_recipe = Recipe.objects.all().order_by("-date_of_creation").filter(status=True)[:5]
    print(_new_recipe)

    best_recipe = Recipe.objects.all().order_by("-num_of_stars").filter(status=True)[:5]
    print(best_recipe)

    context = {
        "sections": [
            ("NEW", combine_recipes_and_photos(_new_recipe)),
            ("BEST", combine_recipes_and_photos(best_recipe))
        ],
        "menu_active": "home",
    }

    return render(request, 'main/index.html', context=context)


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'
    next_page = 'home'
    extra_context = {
        'action': 'login'
    }

    # def get_success_url(self):
    #     return reverse_lazy('home')


class ChangeUserPassword(PasswordChangeView):
    form_class = ChangeUserPasswordForm
    template_name = 'main/change-password.html'

    def get_success_url(self):
        return reverse_lazy('my_recipes')


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


def profile(request, author_slug):
    order_by = request.POST.get("sort", "-date_of_creation")
    author = get_object_or_404(Author, slug=author_slug)
    recipes = Recipe.objects.filter(user=author.user).filter(status=True).order_by(order_by)
    context = {
        "author": author,
        "recipes": combine_recipes_and_photos(recipes),
        "selected_sort": order_by,
    }
    return render(request, 'main/profile.html', context=context)


@login_required(login_url='login')
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES)
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
        categor = request.GET.getlist("category")
        sort = request.GET.get("sort", "-num_of_stars")
        search = request.GET.get("search-input", "")
        prod = request.GET.getlist("product", "")
        isAllergic = request.GET.get("allergic", "false")

        recipes = Recipe.objects.filter(status=True)

        # print("allerg", isAllergic)

        if isAllergic == "true":
            allerg = request.user.author.my_exceptions.all()
            for al in allerg:
                recipes = recipes.exclude(recipeingredient__product__name=al)
        recipes = recipes.filter(title__iregex=search)
        if len(prod) != 0:
            for p in prod:
                recipes = recipes.filter(recipeingredient__product__name__istartswith=p)
        recipes = recipes.order_by(sort)
        if len(categor) != 0:
            rec = []
            for c in categor:
                rec = merge_cat(rec, list(recipes.filter(categories__name=c).order_by(sort)))
            recipes = rec
    else:
        recipes = Recipe.objects.all().order_by("-num_of_stars")

    paginator = Paginator(recipes, CART_ON_PAGE)
    page_num = request.GET.get('page_num')
    print("page_num: ", page_num)
    page_obj = paginator.get_page(page_num)

    if is_ajax(request):
        print("Ajax-request")
        cart_list = ""
        for r, r_photo in combine_recipes_and_photos(page_obj.object_list):
            cart_list += render_to_string("main/recipe_cart.html", {"recipe": r, "r_photo": r_photo}, request)
        next_page = None
        try:
            next_page = page_obj.next_page_number()
        except InvalidPage:
            pass
        return JsonResponse({"cart_list": cart_list, "next_page": next_page}, encoder=None)

    if len(recipes) == 0:
        is_data = False
    else:
        is_data = True
    context = {
        "menu_active": "catalogue",
        'recipes': combine_recipes_and_photos(page_obj.object_list),
        'category': Category.objects.filter(parent_category=None),
        'sub_category': Category.objects.all(),
        'selected_categories': categor,
        'categories_hierarchy': Category.get_hierarchy(),
        'selected_sort': sort,
        'curr_search': search,
        'is_data_exist': is_data,
        'prod_types': ProductType.objects.all(),
        'products': Product.objects.all(),
        'selected_products': prod,
        'allergic_on': isAllergic,
        'page_obj': page_obj,
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
    is_liked = False
    is_bookmark = False
    if request.user.is_authenticated:
        liked_recipe = request.user.author.likedrecipe_set.filter(recipe=recp)
        is_liked = liked_recipe.filter(liked_type="L").count() > 0
        is_bookmark = liked_recipe.filter(liked_type="B").count() > 0
    context = {
        'recipe': recp,
        'comments': comments,
        "is_liked": is_liked,
        "is_bookmark": is_bookmark
    }
    return render(request, 'main/recipe.html', context=context)


@login_required(login_url='login')
def my_recipes(request):
    recipes = Recipe.objects.filter(user=request.user).filter(status=True)
    context = {
        'recipes': combine_recipes_and_photos(recipes),
        'active': 'Мои рецепты'
    }
    return render(request, 'main/my_profile.html', context=context)


@login_required(login_url='login')
def my_drafts(request):
    recipes = Recipe.objects.filter(user=request.user).filter(status=False)
    context = {
        'recipes': combine_recipes_and_photos(recipes),
        'active': 'Черновики'
    }
    return render(request, 'main/my_profile.html', context=context)


@login_required(login_url='login')
def my_liked(request):
    recipes = Recipe.objects.filter(likedrecipe__user=request.user.author, likedrecipe__liked_type='L')
    context = {
        'recipes': combine_recipes_and_photos(recipes),
        'active': 'Понравившиеся'
    }
    return render(request, 'main/my_profile.html', context=context)


@login_required(login_url='login')
def my_bookmarks(request):
    recipes = Recipe.objects.filter(likedrecipe__user=request.user.author, likedrecipe__liked_type='B')
    context = {
        'recipes': combine_recipes_and_photos(recipes),
        'active': 'Закладки'
    }
    return render(request, 'main/my_profile.html', context=context)


def numerate_exceptions(exceptions):
    result_list = []
    i = 1
    for e in exceptions:
        result_list.append((i, e))
        i += 1
    return result_list


@login_required(login_url='login')
def my_exceptions(request):
    exceptions = numerate_exceptions(request.user.author.my_exceptions.all())
    products = Product.objects.all()
    # print(exceptions)
    context = {
        'active': 'Исключения',
        'exceptions': exceptions,
        'products': products,
    }
    return render(request, 'main/my_exceptions.html', context=context)


@login_required(login_url='login')
def delete_exception(request):
    if request.method == "POST":
        exception_id = request.POST.get("exception_id")
        product = Product.objects.get(id=exception_id)
        request.user.author.my_exceptions.remove(product)
        # exception = request.user.author.my_exceptions.get(id=exception_id)
        # print(exception)

    return redirect('my_exceptions')


@login_required(login_url='login')
def add_exception(request):
    if request.method == "POST":
        try:
            prod_name = request.POST.get("prod_name", None)
            product = Product.objects.get(name=prod_name)
            request.user.author.my_exceptions.add(product)
        except ObjectDoesNotExist:
            print("Продукт не найден!")
            pass

    return redirect('my_exceptions')


@login_required(login_url='login')
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
        _recipe.num_of_comments = F('num_of_comments') + 1
        _recipe.save(update_fields=["num_of_comments"])
    return redirect("recipe", recipe_slug)


@login_required(login_url='login')
def delete_comment(request, recipe_slug, comment_id):
    if request.method == "POST":
        print(request.POST)
        comment = get_object_or_404(RecipeComment, pk=comment_id)
        if comment.user == request.user:
            comment_children = comment.get_all_comment_children()
            comment.delete()
            # print(comment_children)
            _recipe = get_object_or_404(Recipe, slug=recipe_slug)
            _recipe.num_of_comments = F('num_of_comments') - 1 - len(comment_children)
            _recipe.save(update_fields=["num_of_comments"])
    return redirect("recipe", recipe_slug)


@login_required(login_url='login')
def stars_on(request):
    # print("ON_STARS_Request: ", request)
    if request.method == "GET":
        try:
            like_type = request.GET.get("type")
            recipe_id = request.GET.get("id")
            # print("type: ", like_type, "id: ", recipe_id)
            user = request.user.author
            _recipe = Recipe.objects.get(id=recipe_id)

            like = LikedRecipe(user=user, recipe=_recipe, liked_type=like_type)
            like.save()

            if like_type == 'L':
                _recipe.num_of_stars = F('num_of_stars') + 1
                _recipe.save(update_fields=["num_of_stars"])
            else:
                _recipe.num_of_bookmarks = F('num_of_bookmarks') + 1
                _recipe.save(update_fields=["num_of_bookmarks"])

            return HttpResponse("OK")
        except:
            return HttpResponse("FAIL")
    return HttpResponse("FAIL")


@login_required(login_url='login')
def stars_off(request):
    # print("OFF_STARS_Request: ", request)
    if request.method == "GET":
        try:
            like_type = request.GET.get("type")
            recipe_id = request.GET.get("id")
            # print("type: ", like_type, "id: ", recipe_id)
            user = request.user.author
            _recipe = Recipe.objects.get(id=recipe_id)
            LikedRecipe.objects.get(user=user, recipe=_recipe, liked_type=like_type).delete()

            if like_type == 'L':
                _recipe.num_of_stars = F('num_of_stars') - 1
                _recipe.save(update_fields=["num_of_stars"])
            else:
                _recipe.num_of_bookmarks = F('num_of_bookmarks') - 1
                _recipe.save(update_fields=["num_of_bookmarks"])

            return HttpResponse("OK")
        except:
            return HttpResponse("FAIL")
    return HttpResponse("FAIL")


@login_required(login_url='login')
def new_recipe(request):
    return render(request, 'main/new_recipe.html')


def main_search(request):
    search = request.GET.get("main-search", "")
    if search:
        recipes = Recipe.objects.filter(Q(title__iregex=search)) \
                  | Recipe.objects.filter(Q(description__iregex=search)) \
                  | Recipe.objects.filter(Q(recipeingredient__product__name__iregex=search)) \
                  | Recipe.objects.filter(Q(categories__name__iregex=search))
        recipes = recipes.distinct()
    else:
        recipes = Recipe.objects.all()

    paginator = Paginator(recipes, CART_ON_PAGE)
    page_num = request.GET.get('page_num')
    print("page_num: ", page_num)
    page_obj = paginator.get_page(page_num)

    if is_ajax(request):
        print("Ajax-request")
        cart_list = ""
        for r, r_photo in combine_recipes_and_photos(page_obj.object_list):
            cart_list += render_to_string("main/recipe_cart.html", {"recipe": r, "r_photo": r_photo}, request)
        next_page = None
        try:
            next_page = page_obj.next_page_number()
        except InvalidPage:
            pass
        return JsonResponse({"cart_list": cart_list, "next_page": next_page}, encoder=None)

    if len(recipes) == 0:
        is_data = False
    else:
        is_data = True
    context = {
        "menu_active": "catalogue",
        'recipes': combine_recipes_and_photos(page_obj.object_list),
        'category': Category.objects.filter(parent_category=None),
        'sub_category': Category.objects.all(),
        'selected_categories': [],
        'categories_hierarchy': Category.get_hierarchy(),
        'selected_sort': "-num_of_stars",
        'curr_search': search,
        'is_data_exist': is_data,
        'prod_types': ProductType.objects.all(),
        'products': Product.objects.all(),
        'selected_products': [],
        'allergic_on': "false",
        'page_obj': page_obj,
    }
    return render(request, 'main/catalogue.html', context=context)


@login_required(login_url='login')
def add_recipe(request):
    print(request)
    print("POST: ", request.POST)
    print("FILES: ", request.FILES)
    if request.method == "POST":
        try:
            title = request.POST.get("title", "Новый Рецепт")
            max_recipe_id = Recipe.objects.aggregate(max_recipe_id=Max('id'))['max_recipe_id']
            slug = slugify(f'{title}-{max_recipe_id + 1}')
            description = request.POST.get("recipe_description", "Описание Рецепта")
            time_list = request.POST.get("cooking_time", "00:00").split(":")
            cooking_time = datetime.timedelta(hours=int(time_list[0]), minutes=int(time_list[1]))
            calories = 0  # calculated
            num_of_servings = int(request.POST.get("num_of_servings", 1))
            finished_product_weight = int(request.POST.get("total-weight", 500))
            dimension = request.POST.get("total-weight-units", 'G')
            status = True if request.POST.get("status", 'to_drafts') == 'publish' else False
            user = request.user

            _new_recipe = Recipe.objects.create(title=title, slug=slug, description=description,
                                                cooking_time=cooking_time, calories=calories,
                                                num_of_servings=num_of_servings,
                                                finished_product_weight=finished_product_weight, dimension=dimension,
                                                status=status, user=user)

            categories = request.POST.getlist("category", [])
            for cat in categories:
                try:
                    category = Category.objects.get(name=cat)
                    while True:
                        _new_recipe.categories.add(category)
                        if category.parent_category is None:
                            break
                        else:
                            category = category.parent_category
                except Exception as e:
                    print(e)
            i = 0
            for m_p in request.FILES.getlist("main_photo", ''):
                try:
                    img_form = LoadMainPhotoForm(request.POST, {"main_photo": m_p})
                    if img_form.is_valid():
                        main_photo = img_form.cleaned_data['main_photo']
                        dot_index = main_photo.name.rfind(".")
                        main_photo.name = slugify(main_photo.name[:dot_index]) + main_photo.name[dot_index:]
                        RecipePhoto.objects.create(photo=main_photo, index=i, recipe=_new_recipe)
                        print("MAIN: ", main_photo.name)
                        i += 1
                    else:
                        print("PROBLEMS WITH PHOTOS")
                except Exception as e:
                    print(e)
            i = 0
            step_title = request.POST.getlist('step-title', [])
            step_description = request.POST.getlist('step-description', [])
            for s_p in request.FILES.getlist("step_photo", ''):
                try:
                    img_form = LoadStepPhotoForm(request.POST, {"step_photo": s_p})
                    if img_form.is_valid():
                        step_photo = img_form.cleaned_data['step_photo']
                        dot_index = step_photo.name.rfind(".")
                        step_photo.name = slugify(step_photo.name[:dot_index]) + step_photo.name[dot_index:]
                        RecipeStep.objects.create(title=step_title[i], index=i, photo=step_photo,
                                                  description=step_description[i], recipe=_new_recipe)
                        print("STEP: ", step_photo.name)
                        i += 1
                    else:
                        print("PROBLEMS WITH PHOTOS")
                except:
                    pass
            i = 0
            product_names = request.POST.getlist('product_name', [])
            product_comments = request.POST.getlist('product_comment', [])
            quantities = request.POST.getlist('quantity', [])
            is_essential_list = request.POST.getlist('is_essential', [])
            all_ingredients_count = len(product_names)
            for p in product_names:
                try:
                    prod = Product.objects.get(name=p)
                    is_essential = True if is_essential_list[i] == "True" else False
                    ingredient = RecipeIngredient.objects.create(comment=product_comments[i], is_essential=is_essential,
                                                                 quantity=quantities[i], index=i+1,
                                                                 main_ingredient=None, recipe=_new_recipe, product=prod)
                    calories += (float(quantities[i]) / 100) * prod.calories
                    analog_names = request.POST.getlist(f'analog-{i+1}-product_name', [])
                    analog_comments = request.POST.getlist(f'analog-{i+1}-product_comment', [])
                    analog_quantities = request.POST.getlist(f'analog-{i+1}-quantity', [])
                    i += 1
                    j = 0
                    for a in analog_names:
                        try:
                            analog = Product.objects.get(name=a)
                            RecipeIngredient.objects.create(comment=analog_comments[j], is_essential=False,
                                                            quantity=analog_quantities[j],
                                                            index=all_ingredients_count,
                                                            main_ingredient=ingredient, recipe=_new_recipe,
                                                            product=analog)
                            all_ingredients_count += 1
                            j += 1
                        except Exception as e:
                            print(e)
                except Exception as e:
                    print(e)
            calories = int((calories * 100) / finished_product_weight) if not(finished_product_weight == 0) else 0
            _new_recipe.calories = calories
            _new_recipe.save()

        except Exception as e:
            print(e)

    return redirect('my_recipes')


def get_products_with_dimension(request):
    if is_ajax(request):
        print("Ajax-request")
        products_dimension = []
        products = Product.objects.all()
        for p in products:
            products_dimension.append((p.name, p.get_dimension_display()))
        return JsonResponse(products_dimension, safe=False)
    return page_not_found()


def get_all_categories(request):
    if is_ajax(request):
        print("Ajax-request")
        categories = []
        for c in Category.objects.all():
            categories.append(c.name)
        return JsonResponse(categories, safe=False)
    return page_not_found()

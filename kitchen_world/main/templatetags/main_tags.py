from django import template
from django.template.loader import render_to_string

from ..models import Category, RecipeComment

register = template.Library()


@register.inclusion_tag('main/recipe_cart.html')
def show_recipe_cart(recipe, r_photo, request, current_page=None):
    is_liked = False
    is_bookmark = False
    if request.user.is_authenticated:
        liked_recipe = request.user.author.likedrecipe_set.filter(recipe=recipe)
        is_liked = liked_recipe.filter(liked_type="L").count() > 0
        is_bookmark = liked_recipe.filter(liked_type="B").count() > 0
    return {"request": request,
            "recipe": recipe,
            "r_photo": r_photo,
            "is_liked": is_liked,
            "is_bookmark": is_bookmark,
            "current_page": current_page}


def is_details_open(selected, hierarchy):
    # print('SELECTED: ', selected, "\nHIERARHY: ", hierarchy)
    is_open = False
    if type(hierarchy) is list:
        for cat in hierarchy:
            if type(cat) is list:
                is_open = is_details_open(selected, cat)
            else:
                is_open = cat.name in selected
            if is_open:
                return True
    else:
        return hierarchy.name in selected
    return is_open


@register.simple_tag()
def show_categories(selected_categories, cat_list):
    menu = ''
    for i in range(len(cat_list)):
        if i < len(cat_list) - 1 and type(cat_list[i + 1]) is list:
            menu += f'<li class="menu__item">' \
                    f'<details'
            if is_details_open(selected_categories, cat_list[i + 1]):
                menu += ' open '
            menu += f'>' \
                    f'  <summary>' \
                    f'  <label class="switch">' \
                    f'      <input  name="category" type="checkbox" value="{cat_list[i].name}" '
            if cat_list[i].name in selected_categories:
                menu += ' checked '
            menu += f'><span class="switch__slider round"></span>' \
                    f'  </label>' \
                    f'{cat_list[i].name}' \
                    f'  </summary>'
        elif type(cat_list[i]) is list:
            menu += f'  {show_categories(selected_categories, cat_list[i])}' \
                    f'</details>' \
                    f'</li>'
        else:
            menu += f'<li class="menu__item">' \
                    f'<label class="switch">' \
                    f'      <input  name="category" type="checkbox" value="{cat_list[i].name}" '
            if cat_list[i].name in selected_categories:
                menu += ' checked '
            menu += f'><span class="switch__slider round"></span>' \
                    f'</label>' \
                    f'{cat_list[i].name}' \
                    f'</li>'
    # print(f'\nStart\n{menu}\nEnd\n')
    return menu


@register.inclusion_tag('main/comment.html')
def show_comment(comment):
    return {"comment": comment}


@register.simple_tag()
def show_all_comments(comments, request):
    html = ""
    for comment in comments:
        html += f'<!-- Comment start -->\n{ render_to_string("main/comment.html", {"comment": comment}, request) }' \
                f'\n <div class="recipe-comment-children">'
        comment_children = RecipeComment.objects.filter(parent_comment=comment)
        html += show_all_comments(comment_children, request)
        html += '\n</div>\n<!-- Comment end -->'
    return html


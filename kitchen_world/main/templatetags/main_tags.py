from django import template

from ..models import Category

register = template.Library()


@register.inclusion_tag('main/recipe_cart.html')
def show_recipe_cart(recipe, r_photo):
    return {"recipe": recipe, "r_photo": r_photo}


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
def show_categories(selected_categories, cat_list=Category.get_hierarchy()):
    menu = ''
    for i in range(len(cat_list)):
        if i < len(cat_list) - 1 and type(cat_list[i + 1]) is list:
            menu += f'<li class="menu__item">' \
                    f'<details'
            if is_details_open(selected_categories, cat_list[i + 1]):
                menu += ' open '
            menu += f'>' \
                    f'  <summary>' \
                    f'      <input  name="category" type="checkbox" value="{cat_list[i].name}" '
            if cat_list[i].name in selected_categories:
                menu += ' checked '
            menu += f'>{cat_list[i].name}' \
                    f'  </summary>'
        elif type(cat_list[i]) is list:
            menu += f'  {show_categories(selected_categories, cat_list[i])}' \
                    f'</details>' \
                    f'</li>'
        else:
            menu += f'<li class="menu__item">' \
                    f'      <input  name="category" type="checkbox" value="{cat_list[i].name}" '
            if cat_list[i].name in selected_categories:
                menu += ' checked '
            menu += f'>{cat_list[i].name}' \
                    f'</li>'
    # print(f'\nStart\n{menu}\nEnd\n')
    return menu

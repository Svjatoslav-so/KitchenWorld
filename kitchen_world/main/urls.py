from django.urls import path
from . import views
from .views import LoginUser

urlpatterns = [
    path('', views.index, name="home"),
    path('login/', LoginUser.as_view(), name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('registration/', views.registration, name="registration"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('catalogue/', views.catalog, name="catalogue"),
    path('recipe/<slug:recipe_slug>', views.recipe, name="recipe"),
    path('my_recipes/', views.my_recipes, name="my_recipes"),
    path('my_drafts/', views.my_drafts, name="my_drafts"),
    path('my_liked/', views.my_liked, name="my_liked"),
    path('my_bookmarks/', views.my_bookmarks, name="my_bookmarks")
]

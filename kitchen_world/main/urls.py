from django.urls import path
from . import views
from .views import LoginUser

urlpatterns = [
    path('', views.index, name="home"),
    path('login/', LoginUser.as_view(), name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('registration/', views.registration, name="registration"),
    path('change-password/', views.ChangeUserPassword.as_view(),
         name="change_password"),
    path('profile/<slug:author_slug>', views.profile, name="profile"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('catalogue/', views.catalog, name="catalogue"),
    path('my_recipes/', views.my_recipes, name="my_recipes"),
    path('my_drafts/', views.my_drafts, name="my_drafts"),
    path('my_exceptions/', views.my_exceptions, name="my_exceptions"),
    path('delete_exception/', views.delete_exception, name="delete_exception"),
    path('add_exception/', views.add_exception, name="add_exception"),
    path('my_liked/', views.my_liked, name="my_liked"),
    path('my_bookmarks/', views.my_bookmarks, name="my_bookmarks"),
    path('recipe/<slug:recipe_slug>', views.recipe, name="recipe"),
    path('recipe/<slug:recipe_slug>/add-comment/', views.add_comment, name="add_comment"),
    path('recipe/<slug:recipe_slug>/delete-comment/<int:comment_id>', views.delete_comment, name="delete_comment"),
    path('stars_on/', views.stars_on, name="stars_on"),
    path('stars_off/', views.stars_off, name="stars_off"),
    path('new_recipe/', views.new_recipe, name="new_recipe"),
]

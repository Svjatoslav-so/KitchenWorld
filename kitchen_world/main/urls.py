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
    path('recipe/<slug:recipe_slug>/add-comment/', views.add_comment, name="add_comment"),
    path('recipe/<slug:recipe_slug>/delete-comment/<int:comment_id>', views.delete_comment, name="delete_comment"),
]

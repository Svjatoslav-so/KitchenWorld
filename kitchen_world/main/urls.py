from django.urls import path
from . import views
from .views import LoginUser

urlpatterns = [
    path('', views.index, name="home"),
    path('login/', LoginUser.as_view(), name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('registration/', views.registration, name="registration"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('recipe/', views.recipe, name="recipe")
]

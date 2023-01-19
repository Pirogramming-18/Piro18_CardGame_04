from django.urls import path
from . import views

app_name = "game"

urlpatterns = [
    path('', views.main_page, name="main"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("game/create", views.game_create, name="create"),
    path("game/<int:pk>/delete", views.game_delete, name="delete"),
]
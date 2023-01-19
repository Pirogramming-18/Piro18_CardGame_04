from django.urls import path
from . import views

app_name = "game"

urlpatterns = [
    path('', views.main_page, name="main"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("list/", views.game_list, name="game_list"),
    path("game/create", views.game_create, name="create"),
    path("<int:pk>", views.game_retrieve, name="game_retrieve"),
    path("defend/<int:pk>", views.defend, name="defend"),
    path("game/<int:pk>/delete", views.game_delete, name="delete"),
    path("ranking_list/", views.ranking_list, name="ranking_list"),
]
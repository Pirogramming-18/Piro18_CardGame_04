from django.urls import path
from . import views

app_name = "game"

urlpatterns = [
    path('', views.main_page, name="main"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("list/", views.game_list, name="game_list"),
    path("<int:pk>/", views.game_retrieve, name="game_retrieve"),
    path("ranking_list/", views.ranking_list, name="ranking_list"),
]
from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from server.apps.game.models import Play, User
import random

def main_page(request, *args, **kwargs):
    return render(request, "game/main.html")

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)      
            return render(request, template_name="game/success.html")
        else:
            return redirect('game:signup')
    else:
        form = SignupForm()
        context = {
            'form': form,
        }
        return render(request, template_name='game/signup.html', context=context)


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            return redirect('game:main')
        else:
            context = {
                'form': form,
            }
            return render(request, template_name='game/login.html', context=context)
    else:
        form = AuthenticationForm()
        context = {
            'form': form,
        }
        return render(request, template_name='game/login.html', context=context)


def logout(request):
    auth.logout(request)
    return redirect('game:main')

def game_create(request, *args, **kwargs):
    # num = random.randint(0, 1)
    # win_list = ["숫자가 더 작은 사람이 대결에서 이깁니다", "숫자가 더 큰 사람이 대결에서 이깁니다"]
    user_id = request.user
    users = User.objects.all()
    card_list = []
    num = 5
    while num > 0:
        number = random.randint(1, 10)
        if number not in card_list:
            card_list.append(number)
            num-=1
        else:
            continue
    card_list.sort()
    num = request.GET.get('search_mode')
    if request.method == "POST":
        Play.objects.create(
            attack_id=user_id,
            defend_id=request.POST["user"],
            attack_card = num,
            defend_card = 0,
            winner = 0,
            rule = 0,
        )
        return redirect("/")
    context = {
        "card_list" : card_list,
        "users" : users,
    }
    return render(request, "game/create_fight.html", context=context)

def game_delete(request, pk, *args, **kwargs):
    if request.method == "POST":
        play = Play.objects.get(id=pk)
        play.delete()
    return redirect("/")
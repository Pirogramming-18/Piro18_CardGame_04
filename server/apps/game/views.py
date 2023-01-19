from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth

# seoyeong
from .models import *
from random import *
#

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

# game update (반격하기)
def defend(request, pk, *args, **kwargs):
    play=Play.objects.get(id=pk)
    
    # 랜덤 숫자 5개
    card_nums=[]
    for i in range(5):
        defend_card_num=randint(1,10)
        while defend_card_num in card_nums:
            defend_card_num = randint(1,10)
        card_nums.append(defend_card_num)
        card_nums.sort()
    
    if request.method == "POST":
        play.defend_card=request.POST["defend_card"]
        play_result(play)
        return redirect("game/game_retrieve.html")

    context= {
        "play":play ,
        "card_nums":card_nums ,
    }
    return render(request, "game/update_counterupdate.html",context=context)

# game result update
def play_result(play):
    play.rule = randint(0,1)
    # 작을때 이김
    if play.rule == 0:
        if play.defend_card > play.attack_card:
            play.winner=play.attack_id
            play.attack_id.score+=play.attack_card
            play.defend_id.score-=play.defend_card
        else:
            play.winner=play.defend_card_id
            play.attack_id.score-=play.attack_card
            play.defend_id.scord+=play.defend_card
    # 클 때 이김
    else:
        if play.defend_card < play.attack_card:
            play.winner=play.attack_id
            play.attack_id.score+=play.attack_card
            play.defend_id.score-=play.defend_card
        else:
            play.winner=play.defend_card_id
            play.attack_id.score-=play.attack_card
            play.defend_id.scord+=play.defend_card
    play.save()
    play.attack_id.save()
    play.defend_id.save()
    return
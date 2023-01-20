from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from .models import User, Play
from django.db.models import Q
from random import *

def main_page(request, *args, **kwargs):
    return render(request, "game/main.html")

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
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
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
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

def game_list(request):
    if request.user.is_authenticated:
        plays = Play.objects.filter(Q(attack_id=request.user.id)|Q(defend_id=request.user.id)).order_by('-id')
        attacks = []
        defends = []
        for play in plays:
            attacks.append(str(play.attack_id))
            defends.append(str(play.defend_id))
        play_list_name = zip(plays, attacks, defends)
        context = {
            'user': request.user,
            'play_list_name': play_list_name,
        }
        return render(request, template_name='game/game_list.html', context=context)
    else:
        return redirect('game:login')

def game_retrieve(request, pk):
    play = Play.objects.get(id=pk)

    other_name = str(play.attack_id)
    other_card = play.attack_card
    user_card = play.defend_card
    if(request.user.username == str(play.attack_id)):
        other_name = str(play.defend_id)
        other_card = play.defend_card
        user_card = play.attack_card
    context = {
        'play': play,
        'attack_name': str(play.attack_id),
        'defend_name': str(play.defend_id),
        'user_name': request.user.username,
        'user_card': user_card,
        'other_name': other_name,
        'other_card': other_card,
        'user_id': request.user.id,
        'how_to_win': Play.how_to_win[play.rule],
    }
    return render(request, template_name='game/game_retrieve.html', context=context)

def ranking_list(request):
    users = User.objects.all().order_by('-score')
    context = {
        "users": users,
    }
    return render(request, template_name='game/ranking_list.html', context=context)
def game_create(request, *args, **kwargs):
    # num = random.randint(0, 1)
    # win_list = ["숫자가 더 작은 사람이 대결에서 이깁니다", "숫자가 더 큰 사람이 대결에서 이깁니다"]
    users = User.objects.all()
    card_list = []
    num = 5
    while num > 0:
        number = randint(1, 10)
        if number not in card_list:
            card_list.append(number)
            num-=1
        else:
            continue
    card_list.sort()
    if request.method == "POST":
        num = request.POST['search_mode']
        Play.objects.create(
            attack_id=request.user,
            defend_id=User.objects.get(id=request.POST["user"]),
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
    return redirect("game:game_list")

# game update (반격하기)
def defend(request, pk, *args, **kwargs):
    play=Play.objects.get(id=pk)
    
    # 랜덤 숫자 5개
    card_nums=[]
    for i in range(5):
        defend_card_num=randint(1,10)
        while defend_card_num in card_nums or defend_card_num == play.attack_card:
            defend_card_num = randint(1,10)
        card_nums.append(defend_card_num)
        card_nums.sort()
    
    if request.method == "POST":
        play.defend_card=int(request.POST["defend_card"])
        play.accept = True
        play.save()
        play_result(play)
        return redirect(f"/{play.id}")

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
            play.winner = play.attack_id.id
            play.attack_id.score+=play.attack_card
            play.defend_id.score-=play.defend_card
        else:
            play.winner=play.defend_id.id
            play.attack_id.score-=play.attack_card
            play.defend_id.score+=play.defend_card
    # 클 때 이김
    else:
        print(type(play.attack_id), play.attack_id)
        if play.defend_card < play.attack_card:
            play.winner=play.attack_id.id
            play.attack_id.score+=play.attack_card
            play.defend_id.score-=play.defend_card
        else:
            play.winner=play.defend_id.id
            play.attack_id.score-=play.attack_card
            play.defend_id.score+=play.defend_card
    play.save()
    play.attack_id.save()
    play.defend_id.save()
    return

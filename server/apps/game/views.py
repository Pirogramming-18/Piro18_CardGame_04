from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from .models import User, Play
from django.db.models import Q

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
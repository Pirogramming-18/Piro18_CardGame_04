from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth

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
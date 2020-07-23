from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model as user_model
User = user_model()


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'makeuser/signupuser.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'makeuser/signupuser.html', {'form': UserCreationForm, 'error': 'Username is already taken, please choose another one'})
        else:
            return render(request, 'makeuser/signupuser.html', {'form': UserCreationForm, 'error': 'Passwords didn\'t match, please try again'})


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'makeuser/loginuser.html', {'form': AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'makeuser/loginuser.html', {'form': AuthenticationForm, 'error': 'We couldn\'t find user or wrong password, please try again'})
        else:
            login(request, user)
            return redirect('home')


# TODO: add like method for comments
from django.views import generic
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib import messages
from categories.models import Category
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from random import randint
from django.contrib.auth import get_user_model as user_model
User = user_model()


def signupuser(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            messages.warning(request, 'You are already logged in')
            return redirect('home')
        else:
            return render(request, 'users/signupuser.html', {'categories': Category.objects.all()})
    else:
        if request.POST.get('password1') == request.POST.get('password2'):
            try:
                if request.POST.get('homepage_posts'):
                    homepage_posts_category = get_object_or_404(
                        Category, pk=request.POST.get('homepage_posts'))
                else:
                    homepage_posts_category = None
                # Start chat only
                if request.POST.get('chat_only_mode') == 'on':
                    is_chat_only_mode = True
                else:
                    is_chat_only_mode = False
                # End chat only
                user = User.objects.create_user(
                    request.POST.get('username'), password=request.POST.get('password1'), homepage_posts=homepage_posts_category, chat_only_mode=is_chat_only_mode)
                user.save()
                login(request, user)
                return redirect('set_email_and_phone')
            except IntegrityError:
                messages.error(
                    request, 'Username is already taken, please choose another one')
                return redirect('signupuser')
        else:
            messages.error(
                request, 'Passwords didn\'t match, please try again')
            return redirect('signupuser')


class VertificationView(generic.View):
    def get(self, request, uidb64, token):
        return redirect('loginuser')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        if request.GET.get('next'):
            return redirect(request.GET.get('next'))
        else:
            return redirect('home')


def loginuser(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            messages.warning(request, 'You are already logged in')
            return redirect('home')
        else:
            return render(request, 'users/loginuser.html', {'form': AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user is None:
            messages.error(
                request, 'The username that you\'ve entered doesn\'t match any account. Or password didn\'t match')
            return redirect('loginuser')
        else:
            login(request, user)
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            else:
                return redirect('home')


# Confirmation
@login_required
def set_email_and_phone(request):
    return render(request, 'users/set_email_and_phone.html')


# Confirm email
@login_required
def send_email_code(request):
    request.user.email_code = None
    email = request.GET.get('email')
    confirmation_code = randint(100000, 999999)
    send_mail(
        'Dfreemedia email confirmation',
        f'This is your email address confirmation code \n {confirmation_code}',
        'dfreemedia@gmail.com',
        [email],
        fail_silently=False,
    )
    request.user.email_code = confirmation_code
    request.user.save()
    return JsonResponse({})


@login_required
def confirm_email(request):
    user_code = int(request.GET.get('code'))
    if user_code == request.user.email_code:
        request.user.email = request.GET.get('email')
        request.user.email_code = None
        request.user.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'fail'})

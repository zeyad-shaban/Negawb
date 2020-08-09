from .utils import account_activation_token
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.views import generic
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import get_user_model as user_model
User = user_model()


def signupuser(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            messages.warning(request, 'You are already logged in')
            return redirect('home')
        else:
            return render(request, 'users/signupuser.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'], password=request.POST['password1'])
                if request.POST['email']:
                    user.is_active = False
                    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                    domain = get_current_site(request).domain
                    link = reverse('activate', kwargs={
                        'uidb64': uidb64, 'token': account_activation_token.make_token(user)})
                    #! CHANGE TO HTTPS WHEN DEVELOPMENT
                    # TODO TO HTTPS WHEN DEVELOPMENT
                    activate_url = f'http://{domain}{link}'
                    email_body = f'{user.username} You are one step away from activating your account, just click this link to vertify your account \n {activate_url} \n Thanks for joining DFreeMedia Community'
                    email = EmailMessage(
                        subject='Activate Your DFreeMedia Account',
                        body=email_body,
                        from_email='dfreemedia@gmail.com',
                        to=(request.POST.get('email'),),
                    )
                    email.send(fail_silently=False)
                else:
                    user.save()
                    login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('home')
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
            request, username=request.POST['username'], password=request.POST['password'])
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

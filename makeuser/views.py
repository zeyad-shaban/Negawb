from django.core.mail import EmailMessage
from .tokens import account_activation_token
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
# email stuff


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'makeuser/signupuser.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'], password=request.POST['password1'])
                if request.POST['email']:
                    user.is_active = False
                    current_site = get_current_site(request)
                    mail_subject = 'Activate your blog account.'
                    message = render_to_string('makeuser/acc_active_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    })
                    to_email = request.POST['email']
                    email = EmailMessage(
                        mail_subject, message, to=[to_email]
                    )
                    email.send()
                    return HttpResponse('Please confirm your email address to complete the registration')

                user.save()
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('home')
            except IntegrityError:
                messages.error(
                    request, 'Username is already taken, please choose another one')
                return redirect('makeuser:signupuser')
        else:
            messages.error(
                request, 'Passwords didn\'t match, please try again')
            return redirect('makeuser:signupuser')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        if request.GET.get('next'):
            return redirect(request.GET.get('next'))
        else:
            return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        if request.GET.get('next'):
            return redirect(request.GET.get('next'))
        else:
            return redirect('home')


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'makeuser/loginuser.html', {'form': AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(
                request, 'The username that you\'ve entered doesn\'t match any account. Or password didn\'t match')
            return redirect('makeuser:loginuser')
        else:
            login(request, user)
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            else:
                return redirect('home')


# TODO: add like method for comments

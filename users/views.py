# from .utils import account_activation_token
from django.urls import reverse
from django.core.mail import EmailMessage
from django.views import generic
from django.template.loader import render_to_string
# from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib import messages
from categories.models import Category
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
                    homepage_posts_category = get_object_or_404(Category, pk=request.POST.get('homepage_posts'))
                else:
                    homepage_posts_category = None
                user = User.objects.create_user(
                    request.POST.get('username'), password=request.POST.get('password1'), homepage_posts=homepage_posts_category)
                if False:
                    pass
                    # user.is_active = False
                    # uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                    # domain = get_current_site(request).domain
                    # link = reverse('activate', kwargs={
                    #     'uidb64': uidb64, 'token': account_activation_token.make_token(user)})
                    # #! CHANGE TO HTTPS WHEN DEVELOPMENT
                    # # TODO TO HTTPS WHEN DEVELOPMENT
                    # activate_url = f'http://{domain}{link}'
                    # email_body = f'{user.username} You are one step away from activating your account, just click this link to vertify your account \n {activate_url} \n Thanks for joining DFreeMedia Community'
                    # email = EmailMessage(
                    #     subject='Activate Your DFreeMedia Account',
                    #     body=email_body,
                    #     from_email='dfreemedia@gmail.com',
                    #     to=(request.POST.get('email'),),
                    # )
                    # email.send(fail_silently=False)
                else:
                    user.save()
                    messages.success(request, 'To allow notifications go <a href="/userpage/">here</a> and click subscribe to push messaging')
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

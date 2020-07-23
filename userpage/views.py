from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from comments.models import Comment, Reply
from people.models import FriendRequest
from django.contrib import messages
from .forms import UserForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model as user_model
User = user_model()


@login_required
def home(request):
    user = request.user
    form = UserForm(instance=request.user)
    if request.method == 'GET':
        return render(request, 'userpage/index.html', {'user': user, 'form': form})
    else:
        try:
            validate_email(request.POST['email'])
            form = UserForm(data=request.POST,
                            files=request.FILES, instance=request.user)
            form.save()
            messages.success(request, 'Updated successfully')
            return redirect('userpage:home')
        except ValidationError:
            messages.warning(request, 'Invalid email address')
            return redirect('userpage:home')
        except:
            messages.warning(
                request, 'unknown error occured, please make sure all your data are correct')
            return redirect('userpage:home')


def questions(request):
    questions = Comment.objects.filter(user=request.user)
    return render(request, 'userpage/questions.html', {'questions': questions})


def friends(request):
    friends = User.objects.filter(friends=request.user)
    return render(request, 'userpage/friends.html', {'friends': friends})


def friendrequests(request):
    requests = FriendRequest.objects.filter(to_user=request.user)
    if request.method == 'GET':
        return render(request, 'userpage/friendrequest.html', {'requests': requests})


def denyrequest(request, request_id):
    denied_request = get_object_or_404(FriendRequest, pk=request_id)
    denied_request.delete()
    messages.success(request, 'Friend Request denied')
    return redirect('userpage:friendrequests')


def requestssent(request):
    requests = FriendRequest.objects.filter(from_user=request.user)
    return render(request, 'userpage/requestssent.html', {'requests': requests})


def acceptrequest(request, request_id):
    friend_request = get_object_or_404(FriendRequest, pk=request_id)
    from_user = request.user
    to_user = friend_request.from_user

    from_user.friends.add(to_user)
    to_user.friends.add(from_user)
    friend_request.delete()
    messages.success(request, f'{to_user} is now a friend')
    return redirect('userpage:friendrequests')



def update_avatar(request):
    request.user.avatar = request.POST['avatar']
    request.user.save()
    messages.success(request, 'Updated Avatar Successfuly')
    messages.info(request, request.user.avatar)
    return redirect('userpage:home')

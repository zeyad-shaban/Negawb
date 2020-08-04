from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from comments.models import Post, Reply
from .models import FriendRequest
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from django.core.serializers import serialize
from django.contrib.auth import get_user_model as user_model
User = user_model()


def people(request, people_id):
    """ View Other Users Accounts """
    view_user = get_object_or_404(User, pk=people_id)
    friends = User.objects.filter(friends=view_user)
    return render(request, 'people/index.html', {'view_user': view_user, 'friends': friends, })


def people_questions(request, peoplequestions_id):
    user = get_object_or_404(User, pk=peoplequestions_id)
    questions = Post.objects.filter(user=user)
    return render(request, 'people/peoplequestions.html', {'questions': questions})

@login_required
def all_people(request):
    users = User.objects.all().order_by('-id')
    user_friends = User.objects.filter(friends=request.user)
    return render(request, 'people/all_people.html', {'users': users, 'user_friends': user_friends, })


def all_peopleresults(request):
    query = request.GET.get('q')
    # todo add phone number query
    results = User.objects.filter(
        Q(username__icontains=query) | Q(email__icontains=query))
    return JsonResponse({'results': serialize('json', results)})


@login_required
def addfriend(request, user_id):
    from_user = request.user
    to_user = get_object_or_404(User, pk=user_id)
    friend_request_check_1 = FriendRequest.objects.filter(
        from_user=from_user, to_user=to_user)
    friend_request_check_2 = FriendRequest.objects.filter(
        from_user=to_user, to_user=from_user)
    if user_id == request.user.id:
        users = User.objects.all()
        message = {
            'text': 'Adding yourself 😭😿',
            'tags': 'error'
        }
        return JsonResponse({'message': message})
    elif friend_request_check_1:
        message = {
            'text': f'You already send a friend request to {to_user}',
            'tags': 'warning',
        }
        return JsonResponse({'message': message})
    elif friend_request_check_2:
        message = {
            'text': f'{to_user} has already send a you a <a href="/userpage/friendrequests/" >friend request Here</a>',
            'tags': 'warning',
        }
        return JsonResponse({'message': message})

    else:
        try:
            friend_request = FriendRequest(
                from_user=from_user, to_user=to_user)
            friend_request.save()
            message = {
                'text': f'Successfully sent Friend request to {to_user}',
                'tags': 'success',
            }
            return JsonResponse({'message': message})
        except:
            users = User.objects.all()
            message = {
                'text': 'Unknown error, please try again and make sure to report a feedback so we can fix this error',
                'tags': 'success',
            }
            return JsonResponse({'message': message})

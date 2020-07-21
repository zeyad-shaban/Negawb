from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from categories.models import Comment, Reply
from .models import FriendRequest
from django.db.models import Q
from django.contrib.auth import get_user_model as user_model
User = user_model()


def people(request, people_id):
    """ View Other Users Accounts """
    user = get_object_or_404(User, pk=people_id)
    return render(request, 'people/index.html', {'user': user})


def people_questions(request, peoplequestions_id):
    user = get_object_or_404(User, pk=peoplequestions_id)
    questions = Comment.objects.filter(user=user)
    return render(request, 'people/peoplequestions.html', {'questions': questions})


def all_people(request):
    users = User.objects.all()
    return render(request, 'people/all_people.html', {'users': users})


def all_peopleresults(request):
    query = request.GET.get('q')
    results = User.objects.filter(Q(username__icontains=query))
    return render(request, 'people/all_peopleresults.html', {'results': results, 'query': query})

@login_required
def addfriend(request, user_id):
    from_user = request.user
    to_user = get_object_or_404(User, pk=user_id)
    if user_id == request.user.id:
        users = User.objects.all()
        return render(request, 'people/all_people.html', {'users': users, 'error': "Adding yourself 😭😿"})
    else:
        try:
            friend_request = FriendRequest(
                from_user=from_user, to_user=to_user)
            friend_request.save()
            return redirect('people:all_people')
        except:
            users = User.objects.all()
            return render(request, 'people/all_people.html', {'users': users, 'error': 'something went wrong'})

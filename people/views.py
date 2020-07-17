from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from categories.models import Comment, Reply
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import FriendRequestForm

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
    return render(request, 'people/all_people.html', {'users': users, 'form':FriendRequestForm})


def all_peopleresults(request):
    query = request.GET.get('q')
    results = User.objects.filter(Q(username__icontains=query))
    return render(request, 'people/all_peopleresults.html', {'results':results, 'query':query, 'form':FriendRequestForm})

def addfriend(request, user_id):
    to_user = get_object_or_404(User, pk=user_id)
    return render(request, 'people/addfriend.html', {'to_user':to_user, 'form':FriendRequestForm})
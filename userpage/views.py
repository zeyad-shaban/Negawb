from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from categories.models import Comment, Reply, FriendRequest
from django.contrib.auth.models import User


@login_required
def home(request):
    user = request.user
    return render(request, 'userpage/index.html', {'user': user})


def questions(request):
    questions = Comment.objects.filter(user=request.user)
    return render(request, 'userpage/questions.html', {'questions': questions})


def friendrequests(request):
    requests = FriendRequest.objects.filter(to_user=request.user)
    if request.method == 'GET':
        return render(request, 'userpage/friendrequest.html', {'requests': requests})

def denyrequest(request, request_id):
    denied_request = get_object_or_404(FriendRequest, pk=request_id)
    denied_request.delete()
    return redirect('userpage:friendrequests')
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from categories.models import Comment, Reply
from django.contrib.auth.models import User

@login_required
def home(request):
    user= request.user
    return render(request, 'userpage/index.html', {'user': user})

def questions(request):
    questions = Comment.objects.filter(user=request.user)
    return render(request,'userpage/questions.html',{'questions':questions})


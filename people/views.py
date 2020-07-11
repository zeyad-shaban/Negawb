from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from categories.models import Comment, Reply
from django.contrib.auth.models import User

def people(request, people_id):
    """ View Other Users Accounts """
    user = get_object_or_404(User, pk = people_id)
    return render(request, 'people/index.html', {'user': user})

#todo add people comment
def people_questions(request, people_questions_id):
    questions = Comment.objects.filter(User = people_questions_id)
    return render(request, 'people/peoplequestions.html')
from django.shortcuts import render, redirect
from django.views import generic
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.contrib import messages
from .forms import TodoForm, FeedbackForm
from .models import Feedback


def create_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        todo = form.save(commit=False)
        todo.user = request.user
        todo.save()
        messages.success(request, 'Creted Todo, Good Luck!')
        return JsonResponse({'todo': model_to_dict(todo)}, status=200)


def feedback(request):
    if request.method == 'GET':
        feedbacks = Feedback.objects.all().order_by('-created_date')
        return render(request, 'production/feedback.html', {'form': FeedbackForm, 'feedbacks': feedbacks })
    else:
        form = FeedbackForm(request.POST)
        feedback = form.save(commit=False)
        feedback.user = request.user
        feedback.save()
        messages.success(request, 'Thank you for your feedback, we promise we will read it as soon as possible')
        return redirect('production:feedback')

class ViewFeedback(generic.DetailView):
    model = Feedback
    template_name = 'production/ViewFeedback.html'
from django.shortcuts import render, redirect
from django.views import generic
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.contrib import messages
from .forms import TodoForm, FeedbackForm
from .models import Feedback, Todo


def create_todo(request):
    if request.method == 'GET':
        todo = Todo(title = request.GET.get('title'), note=request.GET.get('note'), is_important = request.GET.get('is_important'), user=request.user)
        todo.save()
        return JsonResponse({'todo': model_to_dict(todo)})


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
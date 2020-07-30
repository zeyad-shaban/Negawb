from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.contrib import messages
from .forms import TodoForm


def create_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        todo = form.save(commit=False)
        todo.user = request.user
        todo.save()
        messages.success(request, 'Creted Todo, Good Luck!')
        return JsonResponse({'todo': model_to_dict(todo)}, status=200)

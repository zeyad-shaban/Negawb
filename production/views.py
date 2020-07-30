from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import TodoForm

def create_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        todo = form.save(commit=False)
        todo.user = request.user
        todo.save()
        messages.success(request, 'Creted Todo, Good Luck!')
        return redirect('home')
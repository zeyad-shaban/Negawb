from production.models import Todo
from production.forms import TodoForm
from social.models import Notification
from django.db.models import Q
from .models import Category


def add_variable_to_context(request):
    try:
        if request.user.is_authenticated:
            todos = Todo.objects.filter(user=request.user, is_completed=False)
            done_todos = Todo.objects.filter(
                user=request.user, is_completed=True)
            # Notifications
            notifications = Notification.objects.filter(
                receiver=request.user).order_by('-date')
            all_categories = []
        else:
            todos = []
            done_todos = []
            notifications = []
            all_categories = Category.objects.all()
    except NameError:
        done_todos = []
        todos = []
        notifications = []

    return {
        'todos': todos,
        'todo_form': TodoForm,
        'done_todos': done_todos,
        'notifications': notifications,
        'all_categories': all_categories,
    }

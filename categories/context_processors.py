from production.models import Todo
from production.forms import TodoForm

def add_variable_to_context(request):
    try:
        if request.user.is_authenticated:
            todos = Todo.objects.filter(user=request.user, is_completed=False)
        else:
            todos = 'Please Log In'
    except NameError:
        todos = 'Please Log In'
    try:
        if request.user.is_authenticated:
            done_todos = Todo.objects.filter(user=request.user, is_completed=True)
        else:
            done_todos = 'Please Log In'
    except NameError:
        todos = 'Please Log In'

    return {
        'todos': todos,
        'todo_form': TodoForm,
        'done_todos': done_todos,
    }

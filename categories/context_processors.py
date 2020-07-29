from production.models import Todo
from production.forms import TodoForm


def add_variable_to_context(request):
    try:
        if request.user.is_authenticated:
            todos = Todo.objects.filter(user=request.user)
        else:
            todos = 'Please Log In'
    except NameError:
        todos = 'Please Log In'

    return {
        'todos': todos,
        'todo_form': TodoForm,
    }

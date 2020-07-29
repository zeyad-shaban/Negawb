from production.models import Todo


def add_variable_to_context(request):

    try:
        if request.user.is_authenticated:
            todos = Todo.objects.filter(user=request.user)
        else:
            todos = 'Please Log In'
    except NameError:
        todos = 'ERROR'

    return {
        'todos': todos,
    }

from social.models import Notification
from .models import Category


def add_variable_to_context(request):
    try:
        if request.user.is_authenticated:
            notifications = Notification.objects.filter(
                receiver=request.user).order_by('-date')
            all_categories = []
        else:
            notifications = []
            all_categories = Category.objects.all()
    except NameError:
        notifications = []

    return {
        'notifications': notifications,
        'all_categories': all_categories,
    }

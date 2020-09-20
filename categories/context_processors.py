from social.models import Notification
from .models import Category


def add_variable_to_context(request):
    try:
        if request.user.is_authenticated:
            notifications = Notification.objects.filter(
                receiver=request.user).order_by('-date')
            unread_notif_count = Notification.objects.filter(
                receiver=request.user, is_read=False).count()
        else:
            notifications = []
            unread_notif_count = []
    except NameError:
        unread_notif_count = []
        notifications = []
    return {
        'notifications': notifications,
        'unread_notif_count': unread_notif_count,
    }

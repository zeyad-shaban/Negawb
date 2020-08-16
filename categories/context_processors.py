from production.models import Todo
from production.forms import TodoForm
from social.models import Notification
from django.db.models import Q


def add_variable_to_context(request):
    try:
        if request.user.is_authenticated:
            todos = Todo.objects.filter(user=request.user, is_completed=False)
            done_todos = Todo.objects.filter(
                user=request.user, is_completed=True)
            # Notifications
            notifications = Notification.objects.filter(
                receiver=request.user).order_by('-date')
            messages_notifications = Notification.objects.filter(Q(receiver=request.user), Q(notification_type='important_friend_message') | Q(
                notification_type='important_group_message') | Q(notification_type='normal_friend_message') | Q(notification_type='normal_group_message')).order_by('-date')
            society_notifications = Notification.objects.filter(Q(receiver=request.user), Q(notification_type='comment_message') | Q(
                notification_type='reply_message')).order_by('-date')
            invites_notifications = Notification.objects.filter(Q(receiver=request.user), Q(
                notification_type='invites')).order_by('-date')
            your_invites_notifications = Notification.objects.filter(Q(receiver=request.user), Q(
                notification_type='your_invites')).order_by('-date')
        else:
            todos = []
            done_todos = []
            notifications = []
            messages_notifications = []
            society_notifications = []
            invites_notifications = []
            your_invites_notifications = []
    except NameError:
        done_todos = []
        todos = []
        notifications = []
        messages_notifications = []
        society_notifications = []
        invites_notifications = []
        your_invites_notifications = []

    return {
        'todos': todos,
        'todo_form': TodoForm,
        'done_todos': done_todos,
        'notifications': notifications,
        'messages_notifications': messages_notifications,
        'society_notifications': society_notifications,
        'invites_notifications': invites_notifications,
        'your_invites_notifications': your_invites_notifications
    }

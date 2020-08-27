from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.contrib import messages
from .forms import TodoForm, FeedbackForm
from .models import Feedback, Todo, Announcement
import datetime
from django.utils.timezone import now




def todo(request):
    if request.GET.get('action') == 'create':
        form = TodoForm(request.GET)
        todo = form.save(commit=False)
        todo.user = request.user
        todo.save()
        message = {
            'text': 'Successfully created todo',
            'tags': 'success',
        }
        return JsonResponse({'todo': model_to_dict(todo), 'message': message})
    elif request.GET.get('action') == 'update':
        # if request.GET.get('pk'):
        # pk = request.GET.get('pk')
        # if request.GET.get('action') == 'check_todo':
        #     todo = get_object_or_404(Todo, pk=pk)
        #     todo.is_completed = True
        #     todo.save()
        #     return JsonResponse({'done': True})
        pass
    else:
        return render(request, 'production/todo.html', {'form':TodoForm})


def feedback(request):
    if request.method == 'GET':
        feedbacks = Feedback.objects.all().order_by('-created_date')
        return render(request, 'production/feedback.html', {'form': FeedbackForm, 'feedbacks': feedbacks})
    else:
        feedbacks_in_last_day = request.user.feedback_set.filter(
            created_date__gt=now() - datetime.timedelta(days=1))
        if feedbacks_in_last_day.count() >= 1:
            messages.error(
                request, 'You can make only 1 feedback each day, please wait till tommorow')
            return redirect('home')
        else:
            form = FeedbackForm(request.POST)
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(
                request, 'Thank you for your feedback, we promise we will read it as soon as possible')
            return redirect('feedback')


class ViewFeedback(generic.DetailView):
    model = Feedback
    template_name = 'production/ViewFeedback.html'


def announcements(request):
    announcements = Announcement.objects.all().order_by('-date')
    return render(request, 'production/announcements.html', {'announcements': announcements})


class ViewAnnounce(generic.DetailView):
    model = Announcement
    template_name = 'production/announce.html'


class About(generic.TemplateView):
    template_name = 'production/about.html'


class Faq(generic.TemplateView):
    template_name = 'production/faq.html'


class TermsAndConditions(generic.TemplateView):
    template_name = 'production/termsandconditions.html'


class PrivacyPolicy(generic.TemplateView):
    template_name = 'production/privacypolicy.html'


class CookiePolicy(generic.TemplateView):
    template_name = 'production/cookiepolicy.html'

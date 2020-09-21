from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.contrib import messages
from .forms import NoteForm, FeedbackForm
from .models import Feedback, Note, Announcement
import datetime
from django.utils.timezone import now


def note(request):
    if request.GET.get('action') == 'create':
        form = NoteForm(request.GET)
        note = form.save(commit=False)
        note.user = request.user
        note.save()
        return JsonResponse({'note': model_to_dict(note)})
    elif request.GET.get('action') == 'update':
        # if request.GET.get('pk'):
        # pk = request.GET.get('pk')
        # if request.GET.get('action') == 'check_note':
        #     note = get_object_or_404(Note, pk=pk)
        #     note.is_completed = True
        #     note.save()
        #     return JsonResponse({'done': True})
        pass
    else:
        return render(request, 'production/note.html', {'form': NoteForm})


def feedback(request):
    if request.method == 'GET':
        feedbacks = Feedback.objects.all().order_by('-date')
        return render(request, 'production/feedback.html', {'form': FeedbackForm, 'feedbacks': feedbacks})
    else:
        form = FeedbackForm(request.POST)
        feedback = form.save(commit=False)
        feedback.user = request.user
        feedback.save()
        messages.success(
            request, 'Thank you for your feedback, we we will read it as soon as possible')
        return redirect('feedback')


def handler404(request, *args, **kwargs):
    return render(request, 'production/404.html')
def handler500(request, *args, **kwargs):
    return render(request, 'production/500.html')



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

from django.forms import ModelForm
from .models import Comment, Reply

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields =['description','title', 'category']

class ReplyForm(ModelForm):
    class Meta:
        model= Reply
        fields= ['description']
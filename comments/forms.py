from django.forms import ModelForm
from .models import Post, Comment

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields =['title','description','image','post_file',]

class CommentForm(ModelForm):
    class Meta:
        model= Comment
        fields= ['description']
from django import forms
from .models import Review, Comment, Photo
from django.forms import ClearableFileInput


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'content','place', 'theme']
        labels = {
            "title": "제목",
            "content": "내용",
            "place":"지역",
            "theme":"테마",
        }
class PhotoForm(forms.ModelForm):
  
    class Meta:
        model = Photo
        fields = ('image', )
        widgets = {
            'image': ClearableFileInput(attrs={'multiple': True}),
        }
class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields=['content',]
        labels = {
            "content": "",
        }
        error_messages = {
            'content': {
                'required':"",
            },
        }
from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['content', 'image']
        widgets={
            'content': forms.Textarea(attrs={'rows':3, 'placeholder': 'What do you think of?'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={
                'placeholder': 'Add a comment...',
                'class': 'form-control'
            })
        }
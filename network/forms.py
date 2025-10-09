from django import forms
from .models import Post, Comment
from .models import Profile

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

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].widget.attrs.update({'class': 'form-control'})
from django import forms
from .models import Post, Comment, Like

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'category', 'tags']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = ['post', 'author']

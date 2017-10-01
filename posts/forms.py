from django import forms

from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "image"
        ]

    # def clean_title(self):
    #     title = self.cleaned_data.get('title')
    #     if len(title) > 120:
    #         raise forms.ValidationError("El titulo no puede contener mas de 120 caracteres.")
    #     return title


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('contenido',)
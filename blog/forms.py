from django import forms
from django.forms import fields
from .models import BlogPost

class CreateBlogPostForm(forms.ModelForm):

    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'image']

class UpdateBlogPostForm(forms.ModelForm):
    class Meta:
        model=BlogPost
        fields=['title', 'body', 'image']

    def save(self, commit=True):
        post = self.instance
        post.title = self.cleaned_data['title']
        post.body=self.cleaned_data['body']

        if self.cleaned_data['image']:
            post.image = self.cleaned_data['image']

        if commit:
            post.save()
        return post
from django import forms
from drafthub.apps.post.models import Post


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'raw_content_url',
        ]


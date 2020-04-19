from django.core.exceptions import ValidationError
from django import forms
from .models import Draft


class DraftForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def clean_title(self):
        from django.utils.text import slugify
        slug = slugify(self.cleaned_data['title'])

        if slug == '-':
            slug = ''

        if not slug:
            raise ValidationError('invalid title')
        
        return self.cleaned_data['title']
        

    def clean_github_url(self):
        import re
        import requests
        from .utils import get_data_from_url

        data = get_data_from_url(self.cleaned_data['github_url'])

        if not data:
            raise ValidationError('url must be a github .md file.')

        login = data['login']
        if login != self.request.user.username:
            raise ValidationError('url must be from your repositories.')

        raw = data['raw']
        head_response = requests.head(raw)
        if head_response.status_code != 200:
            raise ValidationError('not found in your repositories.')

        return self.cleaned_data['github_url']


    class Meta:
        model = Draft
        fields = ['title', 'github_url', 'abstract']

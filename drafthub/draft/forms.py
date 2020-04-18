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

        re_url = '^https?:\/\/github\.com\/(.+)\/(.+)\/blob\/(.*\.md)$'
        match_url = re.compile(re_url)
        match_results = match_url.match(self.cleaned_data['github_url'])
    
        if not match_results:
            raise ValidationError('url must be a github .md file.')

        handle, repo, md = match_results.groups()
        if handle != self.request.user.username:
            raise ValidationError('url must be from your repositories.')

        url_raw = f'https://raw.githubusercontent.com/{handle}/{repo}/{md}'
        head_response = requests.head(url_raw)
        if head_response.status_code != 200:
            raise ValidationError('not found in your repositories.')

        return self.cleaned_data['github_url']


    class Meta:
        model = Draft
        fields = ['title', 'github_url', 'abstract']
